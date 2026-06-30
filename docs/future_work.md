# Future Work & Structured Methodology

## 📋 What's Built vs. What Needs Extension

This document outlines the **structured methodology** for extending the Adaptive Network Switching System beyond its current implementation into a production-grade system.

---

## ✅ Currently Implemented

| Feature | Status | Description |
|---------|--------|-------------|
| WMCDA Scoring Engine v2 | ✅ Complete | Weighted multi-criteria scoring with **Dynamic Stability Penalty** |
| Adaptive Profiles | ✅ Complete | 6 usage profiles with dynamic weight adjustment |
| Real Network Scanning | ✅ Complete | Windows `netsh` integration for live WiFi data |
| Auto-Switching with Hysteresis | ✅ Complete | Background daemon with cooldown and flapping prevention |
| QoS Traffic Routing | ✅ Complete | DSCP tagging via PowerShell `New-NetQosPolicy` per profile |
| REST API + WebSocket | ✅ Complete | FastAPI with scan, profiles, formula, QoS, history endpoints |
| CORS Security | ✅ Complete | Restricted to frontend origins only |
| Subprocess Safety | ✅ Complete | `CREATE_NO_WINDOW` flag on all subprocess calls |
| Duo Minimalist Dashboard | ✅ Complete | Dark charcoal + electric cyan, no glassmorphism |
| Radar Chart Comparisons | ✅ Complete | Recharts-based multi-network comparison |
| Scan History DB | ✅ Complete | SQLite persistence for scan results and switch events |

---

## 🔧 Phase 1: Cross-Platform Support (2-3 weeks)

### 1.1 OS-Level Network Scanning

Extend the scanner to support Linux and macOS:

**Linux:**
```python
def scan_wifi_linux():
    """Use nmcli for Wi-Fi scanning."""
    result = subprocess.run(
        ['nmcli', '-t', '-f', 'SSID,SIGNAL,SECURITY,FREQ,RATE', 'dev', 'wifi', 'list'],
        capture_output=True, text=True
    )
    return parse_nmcli_output(result.stdout)
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

### 1.2 Cross-Platform QoS

- **Linux:** Use `tc` (traffic control) and `iptables` DSCP marking.
- **macOS:** Use `pfctl` or `dnctl` for packet classification.

---

## 🔧 Phase 2: Machine Learning Enhancement (4-6 weeks)

### 2.1 Predictive Network Quality

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

### 2.2 Reinforcement Learning for Switching Policy

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

## 🔧 Phase 3: Advanced Features (Ongoing)

### 3.1 Multi-SIM / Multi-WAN Bonding
- Aggregate bandwidth across multiple connections
- Use MPTCP (Multi-Path TCP) for link aggregation
- Implement failover chains

### 3.2 Per-Application QoS Routing
- Route different traffic types through different networks:
  - Video → highest bandwidth network
  - VoIP → lowest latency network
  - Background sync → cheapest network
- Uses Windows WFP (Windows Filtering Platform) for per-app packet inspection.

### 3.3 Security Enhancements
- VPN auto-connect on untrusted networks
- Certificate-based network authentication
- Rogue AP detection

### 3.4 Edge Computing Integration
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
│  │  │ Scoring  │  │Scanner │  │  QoS   │  │  │
│  │  │ Engine   │  │Service │  │ Router │  │  │
│  │  └──────────┘  └────────┘  └────────┘  │  │
│  │           ┌────────┐                    │  │
│  │           │   DB   │                    │  │
│  │           │(SQLite)│                    │  │
│  │           └────────┘                    │  │
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
- RFC 2474 — Definition of the Differentiated Services Field (DS Field) in the IPv4 and IPv6 Headers
