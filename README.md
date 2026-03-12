# 🚀 Adaptive Network Switching System

> **Next-generation intelligent network selection using Weighted Multi-Criteria Decision Analysis (WMCDA)**

An AI-powered system that analyzes available networks (5G, WiFi 6E, WiFi 6, LTE, Satellite, 3G) and selects the optimal network based on a composite scoring formula with adaptive profiles.

---

## 📸 Features

- **WMCDA Scoring Engine** — Custom formula evaluating 6 network metrics with adaptive weights
- **6 Usage Profiles** — Balanced, Streaming, Gaming, Enterprise, Budget, IoT
- **Real-time Dashboard** — Premium glassmorphism UI with radar charts and live rankings
- **10 Simulated Networks** — Realistic 5G/WiFi/LTE/Satellite networks with dynamic jitter
- **Network Comparison** — Side-by-side radar chart visualization of top networks
- **Scan History** — SQLite-backed persistence of all scans and switch events
- **WebSocket** — Real-time live monitoring endpoint
- **REST API** — Full API with auto-generated OpenAPI docs

---

## 🧮 Scoring Formula

The system uses **Weighted Multi-Criteria Decision Analysis (WMCDA):**

```
CNS = Σ(wi × Ni) / Σ(wi)

Where:
  w₁ = 0.25 × Signal Strength (normalized)
  w₂ = 0.20 × Bandwidth (normalized)
  w₃ = 0.20 × Latency (inverted, normalized)
  w₄ = 0.15 × Reliability (normalized)
  w₅ = 0.10 × Security Level (normalized)
  w₆ = 0.10 × Cost (inverted, normalized)
```

Weights dynamically shift based on the selected usage profile.

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | React + Vite |
| Charts | Recharts |
| Backend | Python FastAPI |
| Database | SQLite |
| Real-time | WebSocket |
| Styling | Custom CSS (Glassmorphism) |

---

## 📁 Project Structure

```
adaptive-network-switching/
├── backend/
│   ├── main.py            # FastAPI server (REST + WebSocket)
│   ├── models.py           # Pydantic data models
│   ├── scoring.py          # WMCDA scoring engine
│   ├── scanner.py          # Network simulator
│   ├── database.py         # SQLite persistence
│   ├── config.py           # Configuration & weights
│   └── requirements.txt    # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── App.jsx         # Main application
│   │   ├── index.css       # Global styles
│   │   └── components/     # React components
│   ├── index.html          # Entry HTML
│   └── package.json        # Node dependencies
├── docs/
│   └── future_work.md      # Extension methodology
└── README.md
```

---

## 🚀 Quick Start

### Prerequisites
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

1. Select a **usage profile** (Balanced, Gaming, Streaming, etc.)
2. Click **📡 Scan Networks**
3. View ranked networks, radar chart, and best recommendation
4. Switch profiles to see how weights change the rankings

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/scan?profile=balanced` | Scan and score networks |
| `POST` | `/api/scan` | Scan with custom weights |
| `GET` | `/api/profiles` | List all usage profiles |
| `GET` | `/api/formula?profile=gaming` | Get scoring formula details |
| `GET` | `/api/history` | Scan and switch history |
| `GET` | `/api/metrics` | Time-series metrics data |
| `GET` | `/api/status` | System status |
| `WS` | `/ws/live` | Real-time monitoring |

---

## 📐 Network Metrics

| Metric | Range | Best Value | Weight (Balanced) |
|--------|-------|------------|-------------------|
| Signal Strength | -100 to -30 dBm | -30 dBm (highest) | 25% |
| Bandwidth | 0 – 10,000 Mbps | 10,000 Mbps | 20% |
| Latency | 1 – 500 ms | 1 ms (lowest) | 20% |
| Reliability | 0 – 100% | 100% | 15% |
| Security Level | 0 – 5 | 5 (strongest) | 10% |
| Cost | $0 – $100/mo | $0 (free) | 10% |

---

## 🔮 Future Extensions

See [`docs/future_work.md`](docs/future_work.md) for structured methodology on:
- Real OS-level network scanning (Windows/Linux/macOS)
- Automatic network switching with hysteresis
- ML-based quality prediction
- Multi-SIM/Multi-WAN bonding
- QoS-aware traffic routing

---

## 📄 License

MIT License — Built for academic and research purposes.
