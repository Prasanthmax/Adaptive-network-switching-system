"""
Real Network Scanner for Windows
=================================
Uses native Windows commands (netsh) to:
  1. Scan visible WiFi networks with signal/band/encryption
  2. Get current connection details (SSID, signal, speed, RSSI)
  3. List saved/known WiFi profiles
  4. Measure real latency via ICMP ping
  5. Measure real throughput via psutil byte counters
  6. Switch networks using netsh wlan connect
"""

import subprocess
import re
import time
import psutil
from typing import List, Optional, Dict, Tuple
from config import SECURITY_LEVELS, RADIO_GENERATIONS, AUTO_SWITCH


# ============================================================================
# NETSH OUTPUT PARSERS
# ============================================================================

def _run_netsh(args: list) -> str:
    """Run a netsh command and return stdout."""
    try:
        result = subprocess.run(
            ["netsh"] + args,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )
        return result.stdout or ""
    except Exception as e:
        print(f"[Scanner] netsh error: {e}")
        return ""


def scan_visible_networks() -> List[dict]:
    """
    Scan all visible WiFi networks using 'netsh wlan show networks mode=bssid'.
    
    Returns list of dicts with:
      ssid, bssid, signal_percent, radio_type, band, channel,
      authentication, encryption, network_type
    """
    output = _run_netsh(["wlan", "show", "networks", "mode=bssid"])
    if not output:
        return []
    
    networks = []
    current_ssid = None
    current_auth = None
    current_encryption = None
    current_net_type = None
    current_bssid_data = None
    
    for line in output.splitlines():
        line = line.strip()
        
        # SSID line
        ssid_match = re.match(r"^SSID\s+\d+\s*:\s*(.+)$", line)
        if ssid_match:
            current_ssid = ssid_match.group(1).strip()
            current_auth = None
            current_encryption = None
            current_net_type = None
            continue
        
        # Network type
        if line.startswith("Network type"):
            current_net_type = line.split(":")[-1].strip()
            continue
        
        # Authentication
        if line.startswith("Authentication"):
            current_auth = line.split(":")[-1].strip()
            continue
        
        # Encryption
        if line.startswith("Encryption"):
            current_encryption = line.split(":")[-1].strip()
            continue
        
        # BSSID line — start a new access point entry
        bssid_match = re.match(r"^BSSID\s+\d+\s*:\s*([0-9a-fA-F:]+)", line)
        if bssid_match:
            current_bssid_data = {
                "ssid": current_ssid or "",
                "bssid": bssid_match.group(1).strip(),
                "authentication": current_auth or "Open",
                "encryption": current_encryption or "None",
                "network_type": current_net_type or "Infrastructure",
                "signal_percent": 0,
                "radio_type": "",
                "band": "",
                "channel": 0,
                "generation": "",
            }
            networks.append(current_bssid_data)
            continue
        
        # Properties under a BSSID
        if current_bssid_data:
            if line.startswith("Signal"):
                sig_match = re.search(r"(\d+)%", line)
                if sig_match:
                    current_bssid_data["signal_percent"] = int(sig_match.group(1))
            
            elif line.startswith("Radio type"):
                radio = line.split(":")[-1].strip()
                current_bssid_data["radio_type"] = radio
                current_bssid_data["generation"] = RADIO_GENERATIONS.get(radio, radio)
            
            elif line.startswith("Band"):
                current_bssid_data["band"] = line.split(":")[-1].strip()
            
            elif line.startswith("Channel"):
                ch_match = re.search(r"(\d+)", line.split(":")[-1])
                if ch_match:
                    current_bssid_data["channel"] = int(ch_match.group(1))
    
    # Merge duplicate BSSIDs for same SSID — keep the one with best signal
    merged = {}
    for net in networks:
        ssid = net["ssid"]
        if ssid not in merged or net["signal_percent"] > merged[ssid]["signal_percent"]:
            merged[ssid] = net
    
    return list(merged.values())


def get_current_connection() -> Optional[dict]:
    """
    Get details of the currently connected WiFi network.
    Uses 'netsh wlan show interfaces'.
    
    Returns dict with:
      ssid, bssid, signal_percent, rssi_dbm, radio_type, band, channel,
      authentication, cipher, receive_rate_mbps, transmit_rate_mbps,
      connection_mode, profile, state, generation
    """
    output = _run_netsh(["wlan", "show", "interfaces"])
    if not output:
        return None
    
    info = {}
    for line in output.splitlines():
        line = line.strip()
        
        if line.startswith("State"):
            info["state"] = line.split(":")[-1].strip()
        elif line.startswith("SSID") and "AP BSSID" not in line:
            info["ssid"] = line.split(":")[-1].strip()
        elif line.startswith("AP BSSID"):
            info["bssid"] = line.split(":", 1)[-1].strip()
        elif line.startswith("Band"):
            info["band"] = line.split(":")[-1].strip()
        elif line.startswith("Channel"):
            ch = re.search(r"(\d+)", line.split(":")[-1])
            info["channel"] = int(ch.group(1)) if ch else 0
        elif line.startswith("Radio type"):
            radio = line.split(":")[-1].strip()
            info["radio_type"] = radio
            info["generation"] = RADIO_GENERATIONS.get(radio, radio)
        elif line.startswith("Authentication"):
            info["authentication"] = line.split(":")[-1].strip()
        elif line.startswith("Cipher"):
            info["cipher"] = line.split(":")[-1].strip()
        elif line.startswith("Receive rate"):
            rate = re.search(r"([\d.]+)", line.split(":")[-1])
            info["receive_rate_mbps"] = float(rate.group(1)) if rate else 0
        elif line.startswith("Transmit rate"):
            rate = re.search(r"([\d.]+)", line.split(":")[-1])
            info["transmit_rate_mbps"] = float(rate.group(1)) if rate else 0
        elif line.startswith("Signal"):
            sig = re.search(r"(\d+)%", line)
            info["signal_percent"] = int(sig.group(1)) if sig else 0
        elif line.startswith("Rssi"):
            rssi = re.search(r"-?\d+", line.split(":")[-1])
            info["rssi_dbm"] = int(rssi.group()) if rssi else 0
        elif line.startswith("Profile"):
            info["profile"] = line.split(":")[-1].strip()
        elif line.startswith("Connection mode"):
            info["connection_mode"] = line.split(":")[-1].strip()
    
    if info.get("state") != "connected":
        return None
    
    return info


def get_saved_profiles() -> List[str]:
    """
    Get list of saved WiFi profile names.
    These are networks the PC has connected to before.
    """
    output = _run_netsh(["wlan", "show", "profiles"])
    if not output:
        return []
    
    profiles = []
    for line in output.splitlines():
        match = re.match(r"\s*All User Profile\s*:\s*(.+)", line)
        if match:
            profiles.append(match.group(1).strip())
    
    return profiles


# ============================================================================
# REAL-TIME MEASUREMENTS
# ============================================================================

def measure_latency(host: str = None, count: int = None) -> dict:
    """
    Measure real network latency using ICMP ping.
    
    Returns dict with: avg_ms, min_ms, max_ms, packet_loss_percent
    """
    host = host or AUTO_SWITCH["latency_test_host"]
    count = count or AUTO_SWITCH["latency_test_count"]
    
    try:
        result = subprocess.run(
            ["ping", "-n", str(count), "-w", "2000", host],
            capture_output=True,
            text=True,
            timeout=count * 3 + 5,
        )
        output = result.stdout
        
        # Parse packet loss
        loss_match = re.search(r"(\d+)%\s+loss", output)
        packet_loss = int(loss_match.group(1)) if loss_match else 100
        
        # Parse timing stats
        stats_match = re.search(
            r"Minimum\s*=\s*(\d+)ms.*Maximum\s*=\s*(\d+)ms.*Average\s*=\s*(\d+)ms",
            output,
        )
        if stats_match:
            return {
                "avg_ms": int(stats_match.group(3)),
                "min_ms": int(stats_match.group(1)),
                "max_ms": int(stats_match.group(2)),
                "packet_loss_percent": packet_loss,
                "host": host,
            }
        
        return {
            "avg_ms": 999,
            "min_ms": 999,
            "max_ms": 999,
            "packet_loss_percent": packet_loss,
            "host": host,
        }
    except Exception as e:
        return {
            "avg_ms": 999,
            "min_ms": 999,
            "max_ms": 999,
            "packet_loss_percent": 100,
            "host": host,
            "error": str(e),
        }


def measure_throughput(duration: float = None) -> dict:
    """
    Measure real network throughput by sampling psutil byte counters.
    
    Samples bytes_sent and bytes_recv over a time window to calculate
    current upload/download speed in Mbps.
    
    Returns dict with: download_mbps, upload_mbps, total_mbps
    """
    duration = duration or AUTO_SWITCH["bandwidth_sample_duration"]
    
    try:
        # Take initial reading
        counters1 = psutil.net_io_counters()
        time.sleep(duration)
        counters2 = psutil.net_io_counters()
        
        # Calculate deltas
        bytes_recv = counters2.bytes_recv - counters1.bytes_recv
        bytes_sent = counters2.bytes_sent - counters1.bytes_sent
        
        # Convert to Mbps
        download_mbps = (bytes_recv * 8) / (duration * 1_000_000)
        upload_mbps = (bytes_sent * 8) / (duration * 1_000_000)
        
        return {
            "download_mbps": round(download_mbps, 2),
            "upload_mbps": round(upload_mbps, 2),
            "total_mbps": round(download_mbps + upload_mbps, 2),
            "bytes_recv": bytes_recv,
            "bytes_sent": bytes_sent,
            "sample_duration_seconds": duration,
        }
    except Exception as e:
        return {
            "download_mbps": 0,
            "upload_mbps": 0,
            "total_mbps": 0,
            "error": str(e),
        }


def measure_throughput_instant() -> dict:
    """
    Quick non-blocking throughput snapshot using psutil.
    Returns cumulative counters (useful for calculating deltas externally).
    """
    try:
        c = psutil.net_io_counters()
        return {
            "bytes_sent": c.bytes_sent,
            "bytes_recv": c.bytes_recv,
            "packets_sent": c.packets_sent,
            "packets_recv": c.packets_recv,
            "errin": c.errin,
            "errout": c.errout,
            "dropin": c.dropin,
            "dropout": c.dropout,
            "timestamp": time.time(),
        }
    except Exception:
        return {"bytes_sent": 0, "bytes_recv": 0, "timestamp": time.time()}


# ============================================================================
# NETWORK SWITCHING
# ============================================================================

def switch_network(ssid: str) -> dict:
    """
    Switch to a saved WiFi network using 'netsh wlan connect'.
    
    Args:
        ssid: The SSID of the network to connect to (must be a saved profile)
    
    Returns:
        dict with success status and message
    """
    try:
        result = subprocess.run(
            ["netsh", "wlan", "connect", f"name={ssid}", f"ssid={ssid}"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=15,
        )
        
        output = (result.stdout or "") + (result.stderr or "")
        success = "successfully" in output.lower() or result.returncode == 0
        
        return {
            "success": success,
            "ssid": ssid,
            "message": output.strip(),
            "timestamp": time.time(),
        }
    except Exception as e:
        return {
            "success": False,
            "ssid": ssid,
            "message": str(e),
            "timestamp": time.time(),
        }


def disconnect_network() -> dict:
    """Disconnect from the current WiFi network."""
    try:
        result = subprocess.run(
            ["netsh", "wlan", "disconnect"],
            capture_output=True, text=True, timeout=10,
        )
        return {"success": True, "message": result.stdout.strip()}
    except Exception as e:
        return {"success": False, "message": str(e)}


# ============================================================================
# COMPREHENSIVE NETWORK SCAN (combines everything)
# ============================================================================

def full_network_scan(measure_speed: bool = True) -> dict:
    """
    Perform a complete network analysis:
      1. Scan all visible WiFi networks
      2. Get current connection details  
      3. Get saved profiles
      4. Measure latency (ping)
      5. Measure throughput (byte counters)
    
    Returns a comprehensive dict with all data.
    """
    # 1. Visible networks
    visible = scan_visible_networks()
    
    # 2. Current connection
    current = get_current_connection()
    
    # 3. Saved profiles  
    saved = get_saved_profiles()
    
    # 4. Mark which visible networks are known (previously connected)
    for net in visible:
        net["is_known"] = net["ssid"] in saved
        net["is_current"] = (
            current is not None and net["ssid"] == current.get("ssid")
        )
    
    result = {
        "visible_networks": visible,
        "current_connection": current,
        "saved_profiles": saved,
        "saved_count": len(saved),
        "visible_count": len(visible),
        "timestamp": time.time(),
    }
    
    # 5. Real-time measurements (only if connected)
    if current and measure_speed:
        latency = measure_latency()
        result["latency"] = latency
        # Use instant counters for non-blocking initial view
        result["throughput_counters"] = measure_throughput_instant()
    
    return result
