# Future Work & Structured Methodology

## 📋 What's Built vs. What Needs Extension

This document outlines the **structured methodology** for extending the Adaptive Network Switching System beyond its current simulation-based implementation into a production-grade real-world system.

---

## ✅ Currently Implemented

| Feature | Status | Description |
|---------|--------|-------------|
| WMCDA Scoring Engine | ✅ Complete | Full weighted multi-criteria decision analysis |
| Adaptive Profiles | ✅ Complete | 6 usage profiles with dynamic weight adjustment |
| Network Simulation | ✅ Complete | 10 realistic network templates with time-of-day jitter |
| REST API | ✅ Complete | FastAPI with scan, profiles, formula, history endpoints |
| WebSocket | ✅ Complete | Real-time network monitoring channel |
| React Dashboard | ✅ Complete | Premium glassmorphism UI with radar charts |
| Scan History DB | ✅ Complete | SQLite persistence for scan results and switch events |

---

## 🔧 Phase 1: Real Network Integration (2-3 weeks)

### 1.1 OS-Level Network Scanning

Replace the simulated scanner with real OS API calls:

**Windows:**
```python
import subprocess
import re

def scan_wifi_windows():
    """Use netsh to scan real WiFi networks."""
    result = subprocess.run(
        ['netsh', 'wlan', 'show', 'networks', 'mode=bssid'],
        capture_output=True, text=True
    )
    # Parse SSID, signal strength, channel, authentication
    networks = parse_netsh_output(result.stdout)
    return networks

def get_cellular_windows():
    """Use Windows Mobile Broadband API for cellular networks."""
    # Use ctypes or win32com to access MBN API
    # Reference: Windows.Networking.Connectivity namespace
    pass
```

**Linux:**
```python
def scan_wifi_linux():
    """Use nmcli for Wi-Fi scanning."""
    result = subprocess.run(
        ['nmcli', '-t', '-f', 'SSID,SIGNAL,SECURITY,FREQ,RATE', 'dev', 'wifi', 'list'],
        capture_output=True, text=True
    )
    return parse_nmcli_output(result.stdout)

def get_cellular_linux():
    """Use ModemManager D-Bus API for cellular."""
    # mmcli -m 0 --signal-get
    pass
```

**macOS:**
```python
def scan_wifi_macos():
    """Use CoreWLAN framework via pyobjc."""
    from CoreWLAN import CWInterface, CWNetwork
    interface = CWInterface.interface()
    networks, error = interface.scanForNetworksWithName_error_(None, None)
    return [parse_cwnetwork(n) for n in networks]
```

### 1.2 Bandwidth & Latency Measurement

```python
import speedtest   # speedtest-cli library
import subprocess

def measure_bandwidth(target_host="8.8.8.8"):
    """Active bandwidth measurement using speedtest or iperf3."""
    st = speedtest.Speedtest()
    st.get_best_server()
    download = st.download() / 1_000_000  # Mbps
    upload = st.upload() / 1_000_000
    return download, upload

def measure_latency(host="8.8.8.8", count=10):
    """Measure round-trip latency using ICMP ping."""
    result = subprocess.run(
        ['ping', '-n', str(count), host],
        capture_output=True, text=True
    )
    # Parse average latency from output
    return parse_ping_output(result.stdout)
```

---

## 🔧 Phase 2: Automatic Network Switching (3-4 weeks)

### 2.1 Platform-Specific Switching

**Windows:**
```powershell
# Connect to a specific WiFi network
netsh wlan connect name="NetworkSSID" ssid="NetworkSSID"

# Switch cellular preference
# Use Windows.Networking.Connectivity API via PowerShell
```

**Linux:**
```bash
# Switch WiFi network
nmcli device wifi connect "NetworkSSID" password "password"

# Set network priority
nmcli connection modify "NetworkSSID" connection.autoconnect-priority 100
```

### 2.2 Seamless Handover Logic

```python
class HandoverManager:
    HYSTERESIS_THRESHOLD = 0.05  # 5% score margin to prevent flapping
    MIN_SWITCH_INTERVAL = 30     # Minimum seconds between switches
    
    def should_switch(self, current_score, candidate_score, last_switch_time):
        """Determine if a network switch is beneficial."""
        time_since_last = time.time() - last_switch_time
        score_improvement = candidate_score - current_score
        
        return (
            score_improvement > self.HYSTERESIS_THRESHOLD and
            time_since_last > self.MIN_SWITCH_INTERVAL
        )
```

---

## 🔧 Phase 3: Machine Learning Enhancement (4-6 weeks)

### 3.1 Predictive Network Quality

Train a model on historical metrics to predict network quality:

```python
from sklearn.ensemble import GradientBoostingRegressor
import pandas as pd

def train_quality_predictor(history_df):
    """Train ML model to predict future network quality."""
    features = ['hour', 'day_of_week', 'signal_strength', 
                'historical_bandwidth_avg', 'congestion_level']
    target = 'composite_score'
    
    model = GradientBoostingRegressor(n_estimators=100, max_depth=5)
    model.fit(history_df[features], history_df[target])
    return model
```

### 3.2 Reinforcement Learning for Switching Policy

```python
# State:  (current_network_metrics, available_networks_metrics, time_features)
# Action: (stay, switch_to_network_i)
# Reward: quality_score - switch_penalty

class NetworkSwitchingAgent:
    def __init__(self):
        self.q_table = {}  # Or use deep Q-network
        self.switch_penalty = 0.1
    
    def get_reward(self, quality_after, did_switch):
        return quality_after - (self.switch_penalty if did_switch else 0)
```

---

## 🔧 Phase 4: Advanced Features (Ongoing)

### 4.1 Multi-SIM / Multi-WAN Bonding
- Aggregate bandwidth across multiple connections
- Use MPTCP (Multi-Path TCP) for link aggregation
- Implement failover chains

### 4.2 QoS-Aware Routing
- Route different traffic types through different networks
- Video → highest bandwidth network
- VoIP → lowest latency network
- Background sync → cheapest network

### 4.3 Security Enhancements
- VPN auto-connect on untrusted networks
- Certificate-based network authentication
- Rogue AP detection

### 4.4 Edge Computing Integration
- MEC (Multi-access Edge Computing) awareness
- Compute offloading decisions based on network quality
- Network slice selection for 5G SA

---

## 📊 Testing Strategy

| Test Type | Tool | Purpose |
|-----------|------|---------|
| Unit Tests | pytest | Scoring algorithm validation |
| Integration Tests | pytest + httpx | API endpoint testing |
| Load Tests | locust | WebSocket scalability |
| Network Simulation | Mininet / NS-3 | Realistic multi-network topologies |
| UI Tests | Playwright | Frontend E2E testing |

---

## 🏗️ Deployment Architecture

```
┌──────────────────────────────────────────────┐
│  User Device                                  │
│  ┌────────────┐  ┌────────────────────────┐  │
│  │  React UI  │  │  Network Agent Service  │  │
│  │  (Browser) │  │  (Background Process)   │  │
│  └─────┬──────┘  └───────────┬────────────┘  │
│        │                     │                │
│        ▼                     ▼                │
│  ┌─────────────────────────────────────────┐  │
│  │     FastAPI Backend (localhost:8000)     │  │
│  │  ┌──────────┐  ┌────────┐  ┌────────┐  │  │
│  │  │ Scoring  │  │Scanner │  │   DB   │  │  │
│  │  │  Engine  │  │Service │  │(SQLite)│  │  │
│  │  └──────────┘  └────────┘  └────────┘  │  │
│  └─────────────────────────────────────────┘  │
└──────────────────────────────────────────────┘
```

---

## 📚 References

- IEEE 802.21 — Media Independent Handover (MIH) standard
- 3GPP TS 23.501 — 5G System Architecture
- MPTCP RFC 8684 — Multi-Path TCP
- TOPSIS — Technique for Order Preference by Similarity
- AHP — Analytic Hierarchy Process
