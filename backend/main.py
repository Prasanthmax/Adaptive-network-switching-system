"""
Adaptive Network Switching System — Real-Time FastAPI Backend
==============================================================
Scans REAL WiFi networks on Windows, measures actual latency/throughput,
scores using WMCDA, and auto-switches when quality drops.
"""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Query
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import asyncio
import json
import time

from models import ScanRequest, SwitchRequest, MonitorControl, UsageProfile
from scanner import (
    scan_visible_networks,
    get_current_connection,
    get_saved_profiles,
    measure_latency,
    measure_throughput,
    measure_throughput_instant,
    full_network_scan,
)
from scoring import score_all_networks, get_formula_explanation
from monitor import monitor
from config import WEIGHT_PROFILES, AUTO_SWITCH

# ============================================================================
# App
# ============================================================================
app = FastAPI(
    title="Adaptive Network Switching System",
    description="Real-time Windows WiFi intelligence with WMCDA scoring",
    version="2.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Start background monitor on startup
@app.on_event("startup")
async def startup():
    print("\n⚡ Adaptive Network Switching System — v2.0 (Real Networks)")
    print("=" * 60)
    print("📡 Scanning REAL WiFi networks on this Windows PC")
    print(f"🔌 API: http://localhost:8000/docs")
    print("=" * 60 + "\n")
    # Note: auto-monitoring starts on user request, not by default


@app.on_event("shutdown")
async def shutdown():
    monitor.stop_monitoring()


# ============================================================================
# API Endpoints
# ============================================================================

@app.get("/")
async def root():
    return {
        "name": "Adaptive Network Switching System",
        "version": "2.0.0 — Real Network Edition",
        "description": "Scans real WiFi networks and auto-switches using WMCDA",
        "platform": "Windows (netsh + psutil)",
    }


@app.get("/api/scan")
async def scan_networks(profile: str = Query("balanced")):
    """
    Scan real WiFi networks, measure latency/throughput, and score using WMCDA.
    This reads actual data from your Windows WiFi adapter.
    """
    # Validate profile
    try:
        usage_profile = UsageProfile(profile)
    except ValueError:
        usage_profile = UsageProfile.BALANCED
    
    monitor.set_profile(usage_profile.value)
    result = monitor.do_scan()
    return result


@app.get("/api/current")
async def get_current():
    """Get details of the currently connected WiFi network."""
    current = get_current_connection()
    if not current:
        return {"connected": False, "message": "No WiFi connection detected"}
    return {"connected": True, **current}


@app.get("/api/visible")
async def get_visible():
    """List all visible WiFi networks (raw scan without scoring)."""
    networks = scan_visible_networks()
    return {"count": len(networks), "networks": networks}


@app.get("/api/profiles")
async def get_profiles():
    """Get all usage profiles with their WMCDA weight configurations."""
    descriptions = {
        "balanced": "Equal priority — ideal for general browsing",
        "streaming": "Prioritizes bandwidth for video/audio streaming",
        "gaming": "Prioritizes low latency for real-time gaming",
        "enterprise": "Emphasizes security and reliability",
        "cost_sensitive": "Maximizes value for cost-conscious usage",
        "iot": "Optimized for IoT — reliability and coverage focused",
    }
    return {
        "profiles": {
            name: {"weights": weights, "description": descriptions.get(name, "")}
            for name, weights in WEIGHT_PROFILES.items()
        }
    }


@app.get("/api/saved")
async def get_saved():
    """List all saved WiFi profiles (previously connected networks)."""
    profiles = get_saved_profiles()
    return {"count": len(profiles), "profiles": profiles}


@app.get("/api/formula")
async def get_formula(profile: str = Query("balanced")):
    """Get the WMCDA formula explanation for a given profile."""
    weights = WEIGHT_PROFILES.get(profile, WEIGHT_PROFILES["balanced"])
    explanation = get_formula_explanation(profile)
    return {
        "profile": profile,
        "weights": weights,
        "formula": explanation,
        "methodology": [
            "1. Scan — Detect visible WiFi networks via Windows netsh",
            "2. Measure — Capture signal %, latency (ping), throughput (psutil bytes)",
            "3. Normalize — Scale all metrics to [0,1] using min-max normalization",
            "4. Weight — Apply profile-adaptive weights to each metric",
            "5. Score — Compute CNS = Σ(wi × Ni) ÷ Σ(wi)",
            "6. Rank — Sort by composite score descending",
            "7. Switch — Auto-connect to best known network if quality drops",
        ],
    }


@app.get("/api/latency")
async def check_latency(host: str = Query("8.8.8.8"), count: int = Query(4, le=10)):
    """Measure real network latency via ICMP ping."""
    result = measure_latency(host, count)
    return result


@app.get("/api/throughput")
async def check_throughput(duration: float = Query(2.0, le=10)):
    """Measure real throughput by sampling psutil byte counters."""
    result = measure_throughput(duration)
    return result


@app.post("/api/switch")
async def switch_to_network(request: SwitchRequest):
    """Manually switch to a specific WiFi network (must be a saved profile)."""
    saved = get_saved_profiles()
    if request.ssid not in saved:
        return {
            "success": False,
            "message": f"'{request.ssid}' is not a saved profile. Connect to it manually first.",
            "saved_profiles": saved[:10],
        }
    
    result = monitor.manual_switch(request.ssid)
    return result


@app.get("/api/monitor/status")
async def monitor_status():
    """Get the background monitor's current status."""
    return monitor.get_status()


@app.post("/api/monitor/start")
async def start_monitor(profile: str = Query("balanced")):
    """Start background network monitoring with auto-switch."""
    try:
        usage_profile = UsageProfile(profile)
    except ValueError:
        usage_profile = UsageProfile.BALANCED
    
    monitor.set_profile(usage_profile.value)
    monitor.auto_switch_enabled = True
    monitor.start_monitoring()
    return {
        "status": "started",
        "profile": usage_profile.value,
        "scan_interval": monitor.scan_interval,
        "auto_switch": monitor.auto_switch_enabled,
    }


@app.post("/api/monitor/stop")
async def stop_monitor():
    """Stop background monitoring."""
    monitor.stop_monitoring()
    return {"status": "stopped"}


@app.post("/api/monitor/configure")
async def configure_monitor(config: MonitorControl):
    """Configure the monitor settings."""
    if config.profile:
        monitor.set_profile(config.profile)
    
    if config.auto_switch:
        monitor.auto_switch_enabled = config.auto_switch.enabled
        monitor.quality_threshold = config.auto_switch.quality_threshold
        monitor.hysteresis_margin = config.auto_switch.hysteresis_margin
        monitor.scan_interval = config.auto_switch.scan_interval_seconds
    
    if config.action == "start":
        monitor.start_monitoring()
    elif config.action == "stop":
        monitor.stop_monitoring()
    
    return monitor.get_status()


# ============================================================================
# WebSocket — Live Real-Time Feed
# ============================================================================

@app.websocket("/ws/live")
async def websocket_live(websocket: WebSocket):
    """
    WebSocket for real-time network monitoring.
    Client sends: {"profile": "balanced"} or {"action": "scan"}
    Server responds with live scan results.
    """
    await websocket.accept()
    
    try:
        while True:
            try:
                data = await asyncio.wait_for(websocket.receive_text(), timeout=None)
                msg = json.loads(data)
            except (json.JSONDecodeError, asyncio.TimeoutError):
                continue
            
            profile = msg.get("profile", monitor.profile)
            monitor.set_profile(profile)
            
            # Do a scan
            result = monitor.do_scan()
            
            # Send compact result
            await websocket.send_text(json.dumps(result, default=str))
            
    except WebSocketDisconnect:
        pass


# ============================================================================
# Entry Point
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
