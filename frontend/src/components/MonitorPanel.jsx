/**
 * MonitorPanel — Shows auto-switch monitor status and switch log.
 */
export default function MonitorPanel({ status, onToggle }) {
    if (!status) return null;

    return (
        <div className="glass-card animate-in delay-5">
            <div className="card-header">
                <div className="card-title">
                    Auto-Switch Monitor
                </div>
                <span className="card-badge" style={{
                    background: status.monitoring ? 'var(--accent-emerald-dim)' : 'var(--accent-rose-dim)',
                    color: status.monitoring ? 'var(--accent-emerald)' : 'var(--accent-rose)',
                    borderColor: status.monitoring ? 'rgba(74, 222, 128, 0.25)' : 'rgba(251, 113, 133, 0.25)',
                }}>
                    {status.monitoring ? 'ACTIVE' : 'STOPPED'}
                </span>
            </div>
            <div className="card-body">
                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '8px', marginBottom: '14px' }}>
                    <InfoBlock label="Scans" value={status.scan_count} />
                    <InfoBlock label="Switches" value={status.switch_count} />
                    <InfoBlock label="Threshold" value={`${(status.quality_threshold * 100).toFixed(0)}%`} />
                    <InfoBlock label="Hysteresis" value={`${(status.hysteresis_margin * 100).toFixed(0)}%`} />
                </div>

                {status.switch_log && status.switch_log.length > 0 && (
                    <div>
                        <div style={{
                            fontSize: '0.65rem',
                            color: 'var(--text-muted)',
                            textTransform: 'uppercase',
                            letterSpacing: '0.06em',
                            marginBottom: '6px',
                            fontWeight: 600,
                        }}>
                            Recent Switches
                        </div>
                        <div style={{ display: 'flex', flexDirection: 'column', gap: '5px' }}>
                            {status.switch_log.slice(-5).reverse().map((log, i) => (
                                <div key={i} style={{
                                    padding: '8px 10px',
                                    background: 'var(--bg-card)',
                                    border: '1px solid var(--border-default)',
                                    borderRadius: 'var(--radius-sm)',
                                    fontSize: '0.72rem',
                                    color: 'var(--text-secondary)',
                                }}>
                                    <div style={{
                                        fontWeight: 700,
                                        color: log.success ? 'var(--accent-emerald)' : 'var(--accent-rose)',
                                    }}>
                                        {log.from_network} to {log.to_network}
                                        {log.success ? ' (Success)' : ' (Failed)'}
                                    </div>
                                    <div style={{
                                        fontSize: '0.6rem',
                                        color: 'var(--text-muted)',
                                        marginTop: '2px',
                                    }}>
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
            background: 'var(--bg-card)',
            border: '1px solid var(--border-default)',
            borderRadius: 'var(--radius-sm)',
            textAlign: 'center',
        }}>
            <div style={{
                fontSize: '0.6rem',
                color: 'var(--text-muted)',
                textTransform: 'uppercase',
                fontWeight: 600,
            }}>
                {label}
            </div>
            <div style={{
                fontSize: '1rem',
                fontWeight: 700,
                fontFamily: "'JetBrains Mono', monospace",
                color: 'var(--text-primary)',
            }}>
                {value}
            </div>
        </div>
    );
}
