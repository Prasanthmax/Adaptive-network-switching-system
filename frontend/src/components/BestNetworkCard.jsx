export default function BestNetworkCard({ best, onSwitch }) {
    if (!best) return null;

    const isConnected = best.is_current;

    return (
        <div className="glass-card animate-in delay-2">
            <div className="card-header">
                <div className="card-title">
                    Best Network
                </div>
                <span className="card-badge">Rank #1</span>
            </div>
            <div className="best-network-card">
                <div className="best-crown" style={{ fontSize: '11px', textTransform: 'uppercase', letterSpacing: '1px', color: 'var(--accent-emerald)', fontWeight: 700, marginBottom: '8px' }}>
                    {isConnected ? 'Active Connection' : 'Optimal Candidate'}
                </div>
                <div className="best-name">{best.ssid}</div>
                <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', fontWeight: 500 }}>
                    {best.generation || best.radio_type} • {best.band} • Ch {best.channel}
                </div>

                <div className="best-score-large">
                    {(best.composite_score * 100).toFixed(1)}
                    <span style={{ fontSize: '1rem', opacity: 0.5 }}>%</span>
                </div>
                <div className="best-score-label">Composite Network Score</div>

                <div className="best-metrics">
                    <div className="best-metric">
                        <div className="best-metric-label">Signal</div>
                        <div className="best-metric-value">{best.signal_percent}%</div>
                    </div>
                    <div className="best-metric">
                        <div className="best-metric-label">Bandwidth</div>
                        <div className="best-metric-value">{best.effective_bandwidth_mbps} Mbps</div>
                    </div>
                    <div className="best-metric">
                        <div className="best-metric-label">Latency</div>
                        <div className="best-metric-value">{best.latency_ms}ms</div>
                    </div>
                    <div className="best-metric">
                        <div className="best-metric-label">Reliability</div>
                        <div className="best-metric-value">{best.reliability_percent}%</div>
                    </div>
                    <div className="best-metric">
                        <div className="best-metric-label">Security</div>
                        <div className="best-metric-value">L{best.security_level}/4</div>
                    </div>
                    <div className="best-metric">
                        <div className="best-metric-label">Stability</div>
                        <div className="best-metric-value">{best.stability_factor ? (best.stability_factor * 100).toFixed(0) : '—'}%</div>
                    </div>
                </div>

                <div className="best-recommendation">{best.recommendation}</div>

                {!isConnected && best.is_known && onSwitch && (
                    <button
                        onClick={() => onSwitch(best.ssid)}
                        style={{
                            marginTop: '16px',
                            padding: '10px 28px',
                            background: 'var(--accent-emerald)',
                            color: '#0D2818',
                            border: '1px solid var(--accent-emerald)',
                            borderRadius: 'var(--radius-sm)',
                            fontSize: '0.82rem',
                            fontWeight: 700,
                            fontFamily: 'inherit',
                            cursor: 'pointer',
                            boxShadow: '0 4px 16px rgba(74, 222, 128, 0.15)',
                        }}
                    >
                        Switch to {best.ssid}
                    </button>
                )}

                {isConnected && (
                    <div style={{
                        marginTop: '16px',
                        padding: '8px 20px',
                        background: 'var(--accent-emerald-dim)',
                        border: '1px solid rgba(74, 222, 128, 0.25)',
                        borderRadius: 'var(--radius-sm)',
                        fontSize: '0.78rem',
                        color: 'var(--accent-emerald)',
                        fontWeight: 700,
                    }}>
                        Currently Connected
                    </div>
                )}
            </div>
        </div>
    );
}
