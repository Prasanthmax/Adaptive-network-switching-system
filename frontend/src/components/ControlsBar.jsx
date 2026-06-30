const PROFILES = [
    { id: 'balanced', label: 'Balanced', desc: 'General use' },
    { id: 'streaming', label: 'Streaming', desc: 'Max bandwidth' },
    { id: 'gaming', label: 'Gaming', desc: 'Low latency' },
    { id: 'enterprise', label: 'Enterprise', desc: 'Security & reliability' },
    { id: 'cost_sensitive', label: 'Budget', desc: 'Lowest cost' },
    { id: 'iot', label: 'IoT', desc: 'Always connected' },
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
            <div style={{ display: 'flex', gap: '8px', marginLeft: 'auto' }}>
                <button
                    className="scan-btn"
                    onClick={() => onMonitorToggle(monitoring ? 'stop' : 'start')}
                    style={{
                        background: monitoring ? 'var(--accent-emerald)' : 'transparent',
                        border: `1px solid ${monitoring ? 'var(--accent-emerald)' : 'var(--border-default)'}`,
                        color: monitoring ? '#0D2818' : 'var(--text-secondary)',
                        boxShadow: monitoring ? '0 4px 16px rgba(74, 222, 128, 0.15)' : 'none',
                    }}
                >
                    {monitoring ? 'Stop Monitor' : 'Auto Monitor'}
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
                        <>Scan Networks</>
                    )}
                </button>
            </div>
        </div>
    );
}
