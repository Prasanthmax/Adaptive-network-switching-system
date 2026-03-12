export default function BestNetworkCard({ best, onSwitch }) {
    if (!best) return null;

    const isConnected = best.is_current;

    return (
        <div className="glass-card animate-in delay-2">
            <div className="card-header">
                <div className="card-title">
                    <span className="icon">🏆</span>
                    Best Network
                </div>
                <span className="card-badge">Rank #1</span>
            </div>
            <div className="best-network-card">
                <div className="best-crown">{isConnected ? '🔗' : '👑'}</div>
                <div className="best-name">{best.ssid}</div>
                <div style={{ fontSize: '0.78rem', color: 'var(--text-muted)' }}>
                    {best.generation || best.radio_type} • {best.band} • Ch {best.channel}
                </div>

                <div className="best-score-large">
                    {(best.composite_score * 100).toFixed(1)}
                    <span style={{ fontSize: '1.2rem', opacity: 0.6 }}>%</span>
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
                        <div className="best-metric-label">Auth</div>
                        <div className="best-metric-value" style={{ fontSize: '0.8rem' }}>{best.authentication}</div>
                    </div>
                </div>

                <div className="best-recommendation">{best.recommendation}</div>

                {!isConnected && best.is_known && onSwitch && (
                    <button
                        onClick={() => onSwitch(best.ssid)}
                        style={{
                            marginTop: '16px',
                            padding: '10px 28px',
                            background: 'linear-gradient(135deg, #10b981, #059669)',
                            color: 'white',
                            border: 'none',
                            borderRadius: 'var(--radius-full)',
                            fontSize: '0.85rem',
                            fontWeight: 600,
                            fontFamily: 'inherit',
                            cursor: 'pointer',
                            boxShadow: '0 0 20px rgba(16, 185, 129, 0.3)',
                        }}
                    >
                        ⚡ Switch to {best.ssid}
                    </button>
                )}

                {isConnected && (
                    <div style={{
                        marginTop: '16px',
                        padding: '8px 20px',
                        background: 'rgba(16, 185, 129, 0.1)',
                        border: '1px solid rgba(16, 185, 129, 0.2)',
                        borderRadius: 'var(--radius-full)',
                        fontSize: '0.8rem',
                        color: '#6ee7b7',
                        fontWeight: 600,
                    }}>
                        ✓ Currently Connected
                    </div>
                )}
            </div>
        </div>
    );
}
