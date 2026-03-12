const PROFILES = [
    { id: 'balanced', label: '⚖️ Balanced', desc: 'General use' },
    { id: 'streaming', label: '🎬 Streaming', desc: 'Max bandwidth' },
    { id: 'gaming', label: '🎮 Gaming', desc: 'Low latency' },
    { id: 'enterprise', label: '🏢 Enterprise', desc: 'Security & reliability' },
    { id: 'cost_sensitive', label: '💰 Budget', desc: 'Lowest cost' },
    { id: 'iot', label: '📟 IoT', desc: 'Always connected' },
];

export default function ControlsBar({ profile, onProfileChange, onScan, scanning, onMonitorToggle, monitoring }) {
    return (
        <div className="controls-bar animate-in">
            <div className="profile-selector">
                {PROFILES.map((p) => (
                    <button
                        key={p.id}
                        className={`profile-btn ${profile === p.id ? 'active' : ''}`}
                        onClick={() => onProfileChange(p.id)}
                        title={p.desc}
                    >
                        {p.label}
                    </button>
                ))}
            </div>
            <div style={{ display: 'flex', gap: '10px', marginLeft: 'auto' }}>
                <button
                    className={`scan-btn ${monitoring ? 'monitoring' : ''}`}
                    onClick={() => onMonitorToggle(monitoring ? 'stop' : 'start')}
                    style={{
                        background: monitoring
                            ? 'linear-gradient(135deg, #10b981, #059669)'
                            : 'var(--bg-glass)',
                        border: monitoring ? 'none' : '1px solid var(--border-glass)',
                        color: monitoring ? 'white' : 'var(--text-secondary)',
                        boxShadow: monitoring ? '0 0 20px rgba(16,185,129,0.3)' : 'none',
                    }}
                >
                    {monitoring ? '🔴 Stop Monitor' : '👁️ Auto Monitor'}
                </button>
                <button
                    className={`scan-btn ${scanning ? 'scanning' : ''}`}
                    onClick={onScan}
                    disabled={scanning}
                >
                    {scanning ? (
                        <>
                            <span className="spinner" />
                            Scanning...
                        </>
                    ) : (
                        <>📡 Scan Networks</>
                    )}
                </button>
            </div>
        </div>
    );
}
