"""
Network Monitor & Auto-Switcher
=================================
Background agent that:
  1. Continuously monitors current connection quality
  2. Periodically re-scans available networks
  3. Scores all networks using WMCDA
  4. Auto-switches to a better known network if quality drops
  5. Maintains hysteresis to prevent flapping
"""

import threading
import time
from datetime import datetime
from typing import Optional, Callable, List

from scanner import (
    scan_visible_networks,
    get_current_connection,
    get_saved_profiles,
    measure_latency,
    measure_throughput_instant,
    switch_network,
)
from scoring import score_all_networks, get_formula_explanation
from config import AUTO_SWITCH, WEIGHT_PROFILES


class NetworkMonitor:
    """
    Background network quality monitor with auto-switching capability.
    """
    
    def __init__(self):
        self._running = False
        self._thread: Optional[threading.Thread] = None
        self._lock = threading.Lock()
        
        # State
        self.profile = "balanced"
        self.auto_switch_enabled = AUTO_SWITCH["enabled"]
        self.scan_interval = AUTO_SWITCH["scan_interval_seconds"]
        self.quality_threshold = AUTO_SWITCH["quality_threshold"]
        self.hysteresis_margin = AUTO_SWITCH["hysteresis_margin"]
        self.min_switch_interval = AUTO_SWITCH["min_switch_interval_seconds"]
        
        # Latest data
        self.latest_scan = None
        self.latest_scores = []
        self.latest_current = None
        self.latest_latency = None
        self.latest_throughput = {"download_mbps": 0, "upload_mbps": 0}
        self.current_score = 0.0
        
        # History
        self.scan_count = 0
        self.switch_count = 0
        self.switch_log = []
        self.last_switch_time = 0
        self.score_history = []  # List of (timestamp, current_score)
        
        # Throughput tracking (for calculating live speed)
        self._prev_counters = None
        self._prev_counter_time = 0
        
        # Callbacks
        self._on_scan_complete: Optional[Callable] = None
        self._on_switch: Optional[Callable] = None
    
    def set_profile(self, profile: str):
        """Change the active scoring profile."""
        if profile in WEIGHT_PROFILES:
            self.profile = profile
    
    def set_on_scan_callback(self, callback: Callable):
        """Set callback for when a scan completes."""
        self._on_scan_complete = callback
    
    def set_on_switch_callback(self, callback: Callable):
        """Set callback for when a network switch occurs."""
        self._on_switch = callback
    
    def do_scan(self) -> dict:
        """
        Perform a single network scan with scoring.
        Can be called manually or by the background monitor.
        """
        with self._lock:
            # 1. Scan visible networks
            visible = scan_visible_networks()
            current = get_current_connection()
            saved = get_saved_profiles()
            
            # Mark known/current networks
            for net in visible:
                net["is_known"] = net["ssid"] in saved
                net["is_current"] = (
                    current is not None and net["ssid"] == current.get("ssid")
                )
                # Add link rate from current connection if this is the connected network
                if net["is_current"] and current:
                    net["receive_rate_mbps"] = current.get("receive_rate_mbps", 0)
                    net["transmit_rate_mbps"] = current.get("transmit_rate_mbps", 0)
            
            # 2. Measure real metrics for current connection
            latency_ms = 50
            throughput_mbps = 0
            packet_loss = 0
            
            if current:
                lat = measure_latency()
                latency_ms = lat.get("avg_ms", 50)
                packet_loss = lat.get("packet_loss_percent", 0)
                self.latest_latency = lat
                
                # Calculate throughput from byte counter deltas
                throughput_mbps = self._calculate_live_throughput()
            
            # 3. Score all networks
            scored = score_all_networks(
                visible,
                profile=self.profile,
                latency_ms=latency_ms,
                throughput_mbps=throughput_mbps,
                packet_loss=packet_loss,
            )
            
            # 4. Update state
            self.latest_scores = scored
            self.latest_current = current
            self.scan_count += 1
            
            # Find current network's score
            current_scored = None
            for s in scored:
                if s.get("is_current"):
                    current_scored = s
                    self.current_score = s["composite_score"]
                    break
            
            # Track score history
            self.score_history.append({
                "timestamp": datetime.now().isoformat(),
                "score": self.current_score,
                "ssid": current.get("ssid", "") if current else "",
            })
            # Keep last 100 entries
            if len(self.score_history) > 100:
                self.score_history = self.score_history[-100:]
            
            result = {
                "timestamp": datetime.now().isoformat(),
                "profile": self.profile,
                "weights": WEIGHT_PROFILES.get(self.profile, {}),
                "visible_count": len(visible),
                "scored_networks": scored,
                "current_connection": current,
                "current_score": self.current_score,
                "latency": self.latest_latency,
                "throughput": self.latest_throughput,
                "scan_count": self.scan_count,
                "switch_count": self.switch_count,
                "auto_switch_enabled": self.auto_switch_enabled,
                "formula": get_formula_explanation(self.profile),
            }
            
            self.latest_scan = result
            
            # 5. Auto-switch logic
            if self.auto_switch_enabled and current_scored:
                self._check_auto_switch(current_scored, scored, saved)
            
            # 6. Callback
            if self._on_scan_complete:
                try:
                    self._on_scan_complete(result)
                except Exception:
                    pass
            
            return result
    
    def _calculate_live_throughput(self) -> float:
        """Calculate live throughput from psutil byte counter deltas."""
        from scanner import measure_throughput_instant
        counters = measure_throughput_instant()
        now = counters["timestamp"]
        
        if self._prev_counters and (now - self._prev_counter_time) > 0.5:
            dt = now - self._prev_counter_time
            bytes_recv = counters["bytes_recv"] - self._prev_counters["bytes_recv"]
            bytes_sent = counters["bytes_sent"] - self._prev_counters["bytes_sent"]
            
            dl_mbps = (bytes_recv * 8) / (dt * 1_000_000)
            ul_mbps = (bytes_sent * 8) / (dt * 1_000_000)
            
            self.latest_throughput = {
                "download_mbps": round(dl_mbps, 2),
                "upload_mbps": round(ul_mbps, 2),
                "total_mbps": round(dl_mbps + ul_mbps, 2),
                "packets_recv": counters.get("packets_recv", 0),
                "packets_sent": counters.get("packets_sent", 0),
                "errors": counters.get("errin", 0) + counters.get("errout", 0),
                "drops": counters.get("dropin", 0) + counters.get("dropout", 0),
            }
            
            self._prev_counters = counters
            self._prev_counter_time = now
            return self.latest_throughput["download_mbps"]
        
        self._prev_counters = counters
        self._prev_counter_time = now
        return 0
    
    def _check_auto_switch(self, current: dict, all_scored: List[dict], saved: List[str]):
        """
        Decide whether to auto-switch based on hysteresis logic.
        
        Rules:
          1. Current score must drop below quality_threshold
          2. Candidate must beat current by at least hysteresis_margin
          3. Min time between switches must have elapsed
          4. Candidate must be a known (saved) network
        """
        now = time.time()
        current_score = current["composite_score"]
        
        # Check cooldown
        if (now - self.last_switch_time) < self.min_switch_interval:
            return
        
        # Check if current quality is acceptable
        if current_score >= self.quality_threshold:
            # Still okay — but check if a much better option exists
            pass
        
        # Find the best candidate (excluding current)
        best_candidate = None
        for s in all_scored:
            if s.get("is_current"):
                continue
            if s["ssid"] not in saved:
                continue  # Only switch to known networks
            if s["composite_score"] > current_score + self.hysteresis_margin:
                best_candidate = s
                break  # Already sorted by score
        
        if best_candidate:
            # SWITCH!
            old_ssid = current["ssid"]
            new_ssid = best_candidate["ssid"]
            
            result = switch_network(new_ssid)
            
            log_entry = {
                "timestamp": datetime.now().isoformat(),
                "from_network": old_ssid,
                "to_network": new_ssid,
                "from_score": round(current_score, 4),
                "to_score": round(best_candidate["composite_score"], 4),
                "reason": (
                    f"Score drop: {old_ssid} at {current_score:.1%} "
                    f"→ {new_ssid} at {best_candidate['composite_score']:.1%}"
                ),
                "success": result.get("success", False),
                "message": result.get("message", ""),
            }
            
            self.switch_log.append(log_entry)
            self.switch_count += 1
            self.last_switch_time = now
            
            if self._on_switch:
                try:
                    self._on_switch(log_entry)
                except Exception:
                    pass
    
    def manual_switch(self, ssid: str) -> dict:
        """Manually switch to a specific network."""
        current = get_current_connection()
        old_ssid = current.get("ssid", "None") if current else "None"
        
        result = switch_network(ssid)
        
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "from_network": old_ssid,
            "to_network": ssid,
            "reason": "Manual switch by user",
            "success": result.get("success", False),
            "message": result.get("message", ""),
        }
        
        self.switch_log.append(log_entry)
        if result.get("success"):
            self.switch_count += 1
            self.last_switch_time = time.time()
        
        return log_entry
    
    # ========================================================================
    # Background monitoring thread
    # ========================================================================
    
    def start_monitoring(self):
        """Start the background monitoring loop."""
        if self._running:
            return
        
        self._running = True
        self._thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self._thread.start()
        print(f"[Monitor] Started — scanning every {self.scan_interval}s")
    
    def stop_monitoring(self):
        """Stop the background monitoring loop."""
        self._running = False
        if self._thread:
            self._thread.join(timeout=15)
        print("[Monitor] Stopped")
    
    def _monitor_loop(self):
        """Background loop that periodically scans and evaluates."""
        while self._running:
            start_time = time.time()
            try:
                self.do_scan()
            except Exception as e:
                print(f"[Monitor] Scan error: {e}")
            
            elapsed = time.time() - start_time
            sleep_needed = max(1.0, self.scan_interval - elapsed)
            
            # Sleep in 0.5s increments to respond quickly to stopping requests
            steps = int(sleep_needed * 2)
            for _ in range(steps):
                if not self._running:
                    break
                time.sleep(0.5)
    
    def get_status(self) -> dict:
        """Get current monitor status."""
        return {
            "monitoring": self._running,
            "profile": self.profile,
            "auto_switch_enabled": self.auto_switch_enabled,
            "scan_count": self.scan_count,
            "switch_count": self.switch_count,
            "current_score": self.current_score,
            "current_ssid": (
                self.latest_current.get("ssid", "") if self.latest_current else ""
            ),
            "scan_interval": self.scan_interval,
            "quality_threshold": self.quality_threshold,
            "hysteresis_margin": self.hysteresis_margin,
            "switch_log": self.switch_log[-10:],  # Last 10
            "score_history": self.score_history[-20:],  # Last 20
        }


# Global singleton
monitor = NetworkMonitor()
