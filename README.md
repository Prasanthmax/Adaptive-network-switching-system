# 🚀 Adaptive Network Switching System

> **Next-generation intelligent real-time network selection using Weighted Multi-Criteria Decision Analysis (WMCDA)**

An AI-powered system that continuously monitors available real WiFi networks on Windows, measures live performance metrics (latency, throughput, signal), and automatically switches to the optimal network based on a composite scoring formula with adaptive profiles.

---

## 📸 Features

- **Real-Time Network Engine** — Interacts with Windows OS (`netsh` & `psutil`) to capture live WiFi data, signal profiles, and byte counters.
- **Auto-Switching with Hysteresis** — Automatically connects to better known networks if current quality drops, while preventing rapid connection flapping.
- **WMCDA Scoring Engine** — Custom formula evaluating 6 network metrics with adaptive weights based on your usage profile.
- **6 Usage Profiles** — Balanced, Streaming, Gaming, Enterprise, Cost Sensitive, IoT.
- **Sleek & Simple Dashboard** — Clean, modern Mist Grey & Midnight Blue UI with radar charts, metric polling, and live network rankings.
- **Live Polling & WebSocket** — Real-time monitoring endpoints to constantly track connection health.
- **REST API** — Full local API backend with auto-generated OpenAPI documentation.

---

## 🧮 Scoring Formula

The system ranks networks locally using **Weighted Multi-Criteria Decision Analysis (WMCDA):**

```
CNS = Σ(wi × Ni) / Σ(wi)

Where:
  w₁ = [Profile] × Signal Strength (normalized to 100%)
  w₂ = [Profile] × Bandwidth/Throughput (measured in Mbps, normalized)
  w₃ = [Profile] × Latency (ping in ms, inverted and normalized)
  w₄ = [Profile] × Reliability (packet delivery ratio, normalized)
  w₅ = [Profile] × Security Level (WEP, WPA2, WPA3, mapped 0-4)
  w₆ = [Profile] × Cost Efficiency (inverted, normalized)
```

Weights dynamically shift based on the selected usage profile.

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| **Frontend** | React, Vite |
| **Styling** | Vanilla CSS (Sleek Mist Grey & Midnight Blue theme) |
| **Charts** | Recharts |
| **Backend** | Python FastAPI |
| **OS Interface** | `subprocess` (netsh), `psutil`, ICMP ping |
| **Database** | SQLite |

---

## 📁 Project Structure

```
adaptive-network-switching/
├── backend/
│   ├── main.py            # FastAPI server (REST + WebSocket)
│   ├── models.py          # Pydantic data models
│   ├── scoring.py         # WMCDA scoring engine
│   ├── scanner.py         # OS-level WiFi scanning & switching
│   ├── monitor.py         # Background daemon for auto-switching
│   ├── database.py        # SQLite persistence
│   ├── config.py          # Configuration & weights
│   └── requirements.txt   # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── App.jsx        # Main application dashboard
│   │   ├── index.css      # Solid Mist Grey / Midnight Blue styles
│   │   └── components/    # React modular components
│   ├── index.html         # Entry HTML
│   └── package.json       # Node dependencies
├── docs/
│   └── future_work.md     # Extension methodology
└── README.md
```

---

## 🚀 Quick Start

### Prerequisites
- Windows OS (required for native `netsh` integration)
- Python 3.9+ 
- Node.js 18+

### 1. Backend Setup

```bash
cd backend
pip install -r requirements.txt
python main.py
```

The API server starts at **http://localhost:8000**  
API docs at **http://localhost:8000/docs**

### 2. Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

The UI opens at **http://localhost:5173**

### 3. Use the App

1. Select a **usage profile** based on your current task (Balanced, Gaming, Streaming, etc.)
2. Click **📡 Scan Networks** to measure real network characteristics.
3. Turn on the **Monitor Panel** to begin tracking connection health in the background. The system will auto-switch to faster networks if your active connection degrades.
4. View real-time radar charting of connection strength, latency, and throughput mapping.

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/scan?profile=balanced` | OS scan to evaluate visible networks |
| `POST` | `/api/switch` | Force switch to known SSID |
| `GET` | `/api/monitor/status` | Read daemon auto-switch status |
| `POST` | `/api/monitor/{start/stop}` | Toggle background hysteresis engine |
| `GET` | `/api/latency` | Run ICMP latency tests |
| `GET` | `/api/throughput` | Run psutil byte-interval sampling |
| `WS` | `/ws/live` | Real-time monitoring data stream |

---

## 📐 Network Metrics

| Metric | Range | Best Value | Weight (Balanced) |
|--------|-------|------------|-------------------|
| Signal Strength | 0 to 100% | 100% | 25% |
| Bandwidth | 0 – 1,000 Mbps | 1,000 Mbps | 20% |
| Latency | 1 – 500 ms | 1 ms (lowest) | 20% |
| Reliability | 0 – 100% | 100% | 15% |
| Security Level | WEP - WPA3 (0 – 4) | WPA3 (Level 4) | 10% |
| Cost | 0.0 - 1.0 (Metered/Free) | 1.0 (free) | 10% |

---

## 🔮 Future Extensions

See [`docs/future_work.md`](docs/future_work.md) for structured methodology on:
- Cross-platform network scanning (Linux `nmcli` / macOS `airport`)
- ML-based predictive network connection quality
- Multi-SIM/Multi-WAN bonding
- QoS-aware application traffic routing

---

## 📄 License

MIT License — Built for academic and research purposes.
