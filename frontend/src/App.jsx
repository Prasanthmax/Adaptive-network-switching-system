import { useState, useCallback, useEffect, useRef } from 'react';
import './index.css';
import Header from './components/Header';
import ControlsBar from './components/ControlsBar';
import StatsRow from './components/StatsRow';
import NetworkList from './components/NetworkList';
import BestNetworkCard from './components/BestNetworkCard';
import RadarChartCard from './components/RadarChartCard';
import FormulaCard from './components/FormulaCard';
import WeightsCard from './components/WeightsCard';
import CurrentConnection from './components/CurrentConnection';
import MonitorPanel from './components/MonitorPanel';

const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8000';

function App() {
  const [profile, setProfile] = useState('balanced');
  const [scanning, setScanning] = useState(false);
  const [scanData, setScanData] = useState(null);
  const [scanCount, setScanCount] = useState(0);
  const [error, setError] = useState(null);
  const [monitorStatus, setMonitorStatus] = useState(null);
  const [menuOpen, setMenuOpen] = useState(false);
  const monitorInterval = useRef(null);

  const handleScan = useCallback(async () => {
    setScanning(true);
    setError(null);
    try {
      const res = await fetch(`${API_BASE}/api/scan?profile=${profile}`);
      if (!res.ok) throw new Error(`Server responded with ${res.status}`);
      const data = await res.json();
      setScanData(data);
      setScanCount((c) => c + 1);
    } catch (err) {
      setError(err.message);
    } finally {
      setScanning(false);
    }
  }, [profile]);

  const handleSwitch = useCallback(async (ssid) => {
    try {
      const res = await fetch(`${API_BASE}/api/switch`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ ssid }),
      });
      const data = await res.json();
      if (data.success) {
        // Ensure UI stays synced with the PC by polling as it connects
        setTimeout(() => handleScan(), 2000);
        setTimeout(() => handleScan(), 5000);
        setTimeout(() => handleScan(), 8000);
      }
      return data;
    } catch (err) {
      return { success: false, message: err.message };
    }
  }, [handleScan]);

  const handleMonitorToggle = useCallback(async (action) => {
    try {
      const res = await fetch(`${API_BASE}/api/monitor/${action}?profile=${profile}`, {
        method: 'POST',
      });
      const data = await res.json();
      setMonitorStatus(data);
    } catch (err) {
      console.error('Monitor error:', err);
    }
  }, [profile]);

  // Fetch initial monitor status to avoid blank area in Dashboard
  useEffect(() => {
    fetch(`${API_BASE}/api/monitor/status`)
      .then(res => res.json())
      .then(data => {
        setMonitorStatus(data);
        if (data.monitoring) {
          handleScan();
        }
      })
      .catch(console.error);
  }, [handleScan]);

  // Poll monitor status when monitoring is active
  useEffect(() => {
    if (monitorStatus?.status === 'started' || monitorStatus?.monitoring) {
      monitorInterval.current = setInterval(async () => {
        try {
          const res = await fetch(`${API_BASE}/api/monitor/status`);
          const data = await res.json();
          setMonitorStatus(data);
          // Also refresh scan data
          if (data.monitoring) {
            const scanRes = await fetch(`${API_BASE}/api/scan?profile=${profile}`);
            const scanResult = await scanRes.json();
            setScanData(scanResult);
            setScanCount((c) => c + 1);
          }
        } catch (err) { /* ignore polling errors */ }
      }, 12000); // Poll every 12 seconds
    }
    return () => {
      if (monitorInterval.current) clearInterval(monitorInterval.current);
    };
  }, [monitorStatus?.monitoring, monitorStatus?.status, profile]);

  const networks = scanData?.scored_networks || [];
  const best = networks.length > 0 ? networks[0] : null;
  const weights = scanData?.weights || null;
  const formula = scanData?.formula || '';
  const current = scanData?.current_connection || null;
  const latency = scanData?.latency || null;
  const throughput = scanData?.throughput || null;

  return (
    <>
      <div className="app-bg" />
      <Header
        scanCount={scanCount}
        lastScan={scanData?.timestamp}
        onMenuToggle={() => setMenuOpen(!menuOpen)}
        menuOpen={menuOpen}
      />

      {/* Slide Panel — Formula & Weights */}
      <div
        className={`slide-panel-backdrop ${menuOpen ? 'open' : ''}`}
        onClick={() => setMenuOpen(false)}
      />
      <aside className={`slide-panel ${menuOpen ? 'open' : ''}`}>
        <div className="slide-panel-header">
          <div className="slide-panel-title">Scoring Engine</div>
          <button className="slide-panel-close" onClick={() => setMenuOpen(false)}>X</button>
        </div>
        <div className="slide-panel-body">
          <FormulaCard formula={formula} />
          <WeightsCard weights={weights} />
        </div>
      </aside>

      <main className="main-content">
        <ControlsBar
          profile={profile}
          onProfileChange={setProfile}
          onScan={handleScan}
          scanning={scanning}
          onMonitorToggle={handleMonitorToggle}
          monitoring={monitorStatus?.monitoring}
        />

        {error && (
          <div className="error-banner">
            Connection error: {error}. Make sure the backend is running on{' '}
            <strong>localhost:8000</strong>.
          </div>
        )}

        {scanData && (
          <>
            <StatsRow
              totalNetworks={scanData.visible_count}
              availableNetworks={networks.length}
              bestScore={best?.composite_score}
              bestName={best?.ssid}
              profile={scanData.profile}
              latency={latency}
              throughput={throughput}
            />

            {current && (
              <CurrentConnection
                connection={current}
                score={scanData.current_score}
                latency={latency}
                throughput={throughput}
              />
            )}

            <div className="dashboard-grid">
              <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
                <NetworkList
                  networks={networks}
                  onSwitch={handleSwitch}
                />
              </div>

              <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
                <BestNetworkCard best={best} onSwitch={handleSwitch} />
                <RadarChartCard networks={networks.slice(0, 5)} />
                <MonitorPanel
                  status={monitorStatus || {}}
                  onToggle={handleMonitorToggle}
                />
              </div>
            </div>
          </>
        )}

        {!scanData && !error && (
          <div className="empty-state animate-in">
            <div className="empty-title">Ready to Scan Real Networks</div>
            <div className="empty-desc">
              Select a usage profile and click <strong>Scan Networks</strong> to
              analyze your <strong>actual WiFi networks</strong> and find the
              optimal connection using WMCDA scoring with real signal, latency,
              and throughput measurements.
            </div>
          </div>
        )}
      </main>
    </>
  );
}

export default App;
