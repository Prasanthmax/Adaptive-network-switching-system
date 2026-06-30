/**
 * MonitorPanel — Shows auto-switch monitor status and switch log.
 */
export default function MonitorPanel({ status, onToggle }) {
    if (!status) return null;

    return (
        <div className="glass-card animate-in delay-5">
            <div className="card-header">
                <div className="card-title">
                    <span className="icon">🤖</span>
                    Auto-Switch Monitor
                </div>
                <span className="card-badge" style={{
                    background: status.monitoring
                        ? 'rgba(16, 185, 129, 0.15)' : 'rgba(244, 63, 94, 0.15)',
                    color: status.monitoring ? '#6ee7b7' : '#fda4af',
                    borderColor: status.monitoring
                        ? 'rgba(16, 185, 129, 0.3)' : 'rgba(244, 63, 94, 0.3)',
                }}>
                    {status.monitoring ? 'ACTIVE' : 'STOPPED'}
                </span>
            </div>
            <div className="card-body">
                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '10px', marginBottom: '16px' }}>
                    <InfoBlock label="Scans" value={status.scan_count} />
                    <InfoBlock label="Switches" value={status.switch_count} />
                    <InfoBlock label="Threshold" value={`${(status.quality_threshold * 100).toFixed(0)}%`} />
                    <InfoBlock label="Hysteresis" value={`${(status.hysteresis_margin * 100).toFixed(0)}%`} />
                </div>

                {status.switch_log && status.switch_log.length > 0 && (
                    <div>
                        <div style={{
                            fontSize: '0.72rem',
                            color: 'var(--text-muted)',
                            textTransform: 'uppercase',
                            letterSpacing: '0.06em',
                            marginBottom: '8px',
                        }}>
                            Recent Switches
                        </div>
                        <div style={{ display: 'flex', flexDirection: 'column', gap: '6px' }}>
                            {status.switch_log.slice(-5).reverse().map((log, i) => (
                                <div key={i} style={{
                                    padding: '8px 12px',
                                    background: 'var(--bg-glass)',
                                    border: '1px solid var(--border-subtle)',
                                    borderRadius: 'var(--radius-sm)',
                                    fontSize: '0.75rem',
                                    color: 'var(--text-secondary)',
                                }}>
                                    <div style={{ fontWeight: 600, color: log.success ? '#6ee7b7' : '#fda4af' }}>
                                        {log.from_network} → {log.to_network}
                                        {log.success ? ' ✓' : ' ✗'}
                                    </div>
                                    <div style={{ fontSize: '0.65rem', color: 'var(--text-muted)', marginTop: '2px' }}>
                                        {log.reason}
                                    </div>
                                </div>
                            ))}
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
}

function InfoBlock({ label, value }) {
    return (
        <div style={{
            padding: '10px',
            background: 'var(--bg-glass)',
            border: '1px solid var(--border-subtle)',
            borderRadius: 'var(--radius-sm)',
            textAlign: 'center',
        }}>
            <div style={{ fontSize: '0.65rem', color: 'var(--text-muted)', textTransform: 'uppercase' }}>
                {label}
            </div>
            <div style={{
                fontSize: '1.1rem',
                fontWeight: 700,
                fontFamily: "'JetBrains Mono', monospace",
                color: 'var(--text-primary)',
            }}>
                {value}
            </div>
        </div>
    );
}
