# Project Report: Adaptive Network Switching System

## 1. Problem Statement
In today's connectivity-driven world, users frequently encounter unstable or suboptimal WiFi connections, characterized by high latency, low throughput, or frequent disconnections. Windows operating systems generally connect to known networks based on signal strength without evaluating the real-time quality of the connection (such as latency, bandwidth, and packet loss). This results in inconsistent operational performance, especially during activities that demand specific network characteristics, like streaming, gaming, or enterprise use. An intelligent, automated solution is required to monitor real-time network health and seamlessly switch to the best available network without manual intervention.

## 2. Introduction
The "Adaptive Network Switching System" is an AI-powered, next-generation network selection tool designed for Windows. It continuously evaluates visible WiFi networks by capturing live performance metrics—including latency, throughput, and signal strength—using native OS tools (`netsh` and `psutil`). Utilizing a custom Weighted Multi-Criteria Decision Analysis (WMCDA) algorithm, the system dynamically ranks networks based on user-selected usage profiles (e.g., Balanced, Streaming, Gaming, Enterprise). When the current connection degrades below a specific threshold, the background hysteresis engine intelligently auto-switches to a superior network while preventing rapid disconnection flapping. 

## 3. Objectives
- **Real-Time Monitoring:** To continuously track network health metrics like throughput, signal strength, latency, packet loss, and security levels.
- **Adaptive Network Scoring:** To implement a WMCDA algorithm that ranks available networks dynamically based on customized profile weights.
- **Automated Network Switching:** To transition seamlessly to the most optimal network available when current connection quality drops, employing hysteresis to ensure stability.
- **User-Centric Configuration:** To provide users with intuitive profiles (Gaming, Streaming, IoT, etc.) that automatically adjust scoring parameters to suit their current activity.
- **Sleek Interface:** To offer a modern, responsive dashboard for real-time visualization of network states, complete with radar charts and live metric polling.

## 4. Modules
The project is divided into distinct modular components, segregating the background tracking engine from the interactive presentation layer:

### Backend Modules (Python/FastAPI)
1. **API & WebSocket Server (`main.py`):** Acts as the central hub, providing RESTful endpoints and real-time WebSocket feeds for the frontend. 
2. **Network Scanner (`scanner.py`):** Interfaces with the Windows OS to capture visible wireless networks, using `netsh` and `psutil` to analyze latency and bandwidth.
3. **Scoring Engine (`scoring.py`):** Contains the WMCDA logic. It normalizes distinct real-time metrics and applies profile-specific weighting to compute the Composite Network Score (CNS).
4. **Background Monitor (`monitor.py`):** A daemon running asynchronously to track connectivity health. It triggers auto-switching logic if the active threshold margin is breached.
5. **Data Persistence (`database.py`):** Built with SQLite, tracks historical network performance.
6. **Data Models & Configuration (`models.py`, `config.py`):** Enforces strict types via Pydantic and stores normalization and default profile bounds.

### Frontend Modules (React/Vite)
1. **Main Dashboard (`App.jsx`):** The central UI integrating various components for user interaction.
2. **Network List & Cards (`NetworkList.jsx`, `BestNetworkCard.jsx`, `CurrentConnection.jsx`):** Renders the scored network list and detailed tiles showing active link metrics.
3. **Data Visualizations (`RadarChartCard.jsx`):** Utilizes `Recharts` to draw dynamic spider charts of current connections.
4. **Controls Panel (`ControlsBar.jsx`, `MonitorPanel.jsx`):** Empowers the user to manually switch networks, trigger scans, activate background monitoring, and switch usage profiles.

## 5. Tech Stack

| Layer | Technology | Description |
|---|---|---|
| **Frontend Framework** | React 19 + Vite | Provides a fast, modular UI. |
| **Styling** | Vanilla CSS | Custom, sleek "Mist Grey & Midnight Blue" theme. |
| **Data Visualization** | Recharts & Framer Motion | Generates interactive radar charts and smooth UI animations. |
| **Backend Framework** | FastAPI (Python) | High-performance API server with native WebSocket support. |
| **OS Interface** | `subprocess` (`netsh`), `psutil`, ICMP | Directly fetches real metrics from the Windows networking adapter. |
| **Database** | SQLite | Lightweight storage for network histories and preferences. |

## 6. Architecture
The architecture follows a decoupled Client-Server model:
- **Client (Frontend):** A React SPA hosted via Vite, communicating with the server down two channels: HTTP REST (for specific commands like scanning, profile changing, or switching) and WebSockets (for a continuous, real-time feed of network statuses).
- **Server (Backend):** A FastAPI instance managing real-world Windows networking interfaces. The `monitor` module operates in a background thread/task, conducting interval sweeps. If a significantly higher-scoring network is found (passing the hysteresis margin), the backend invokes `netsh wlan connect` to auto-switch.
- **Evaluation Flow:** `Scanning → Metric Extraction → Normalization [0, 1] → Profile Weighing → Ranking → Hysteresis Check → Network Switch`.

## 7. Output / Screenshots
*(Please insert the relevant screenshots below)*

1. **Dashboard Overview:** 
   [Insert Screenshot of the main dashboard detailing the Mist Grey / Midnight Blue UI, showing the Radar Chart and Current Connection data]

2. **Available Networks & Rankings:** 
   [Insert Screenshot showing the network list sorted by their Composite Network Score (CNS)]

3. **Monitor Panel Settings:**
   [Insert Screenshot depicting the Monitor control panel, Profile selection (Balanced, Gaming, etc.), and Auto-Switch toggle]

4. **Network Switching Action:**
   [Insert Screenshot (or terminal output) showing the system dynamically switching to a better recognized network]

## 8. Results
The deployment of the Adaptive Network Switching System results in a stable, optimized connectivity experience on Windows. By scoring networks based on practical elements (throughput via byte-interval sampling and ping latency) rather than mere signal strength, connection choices mirror realistic user requirements. The auto-switching hysteresis efficiently prevents the "ping-pong" effect between closely ranking networks, reducing dropout instances. 

## 9. Conclusion
The Adaptive Network Switching System thoroughly redefines how a local client manages its access points. Through the combination of Multi-Criteria Decision Analysis, dynamic user profiling, and direct OS integrations, the application accurately evaluates real-world link conditions. The intuitive dashboard paired with robust, un-intrusive background management serves both novice users and professionals needing guaranteed operational bandwidth or minimal latency. Future expansions could include multi-WAN bonding, macOS/Linux compatibility, or ML-based predictive modeling.
