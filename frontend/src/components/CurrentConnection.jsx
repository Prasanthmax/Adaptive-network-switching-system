/**
 * CurrentConnection — Shows the currently connected WiFi with live metrics.
 */
export default function CurrentConnection({ connection, score, latency, throughput }) {
    if (!connection) return null;

    return (
        <div className="glass-card current-connection animate-in delay-2" style={{ marginBottom: '24px' }}>
            <div className="card-header">
                <div className="card-title">
                    <span className="icon">🔗</span>
                    Currently Connected
                    <span className="live-dot" />
                </div>
                <span className="card-badge" style={{
                    background: 'rgba(16, 185, 129, 0.15)',
                    color: '#6ee7b7',
                    borderColor: 'rgba(16, 185, 129, 0.3)',
                }}>
                    LIVE
                </span>
            </div>
            <div className="card-body" style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(140px, 1fr))', gap: '16px' }}>
                <MetricBox label="SSID" value={connection.ssid} accent />
                <MetricBox label="Signal" value={`${connection.signal_percent}%`} />
                <MetricBox label="RSSI" value={`${connection.rssi_dbm} dBm`} />
                <MetricBox label="Band" value={connection.band} />
                <MetricBox label="Channel" value={connection.channel} />
                <MetricBox label="Radio" value={connection.radio_type} />
                <MetricBox label="Auth" value={connection.authentication} />
                <MetricBox label="Rx Rate" value={`${connection.receive_rate_mbps} Mbps`} />
                <MetricBox label="Tx Rate" value={`${connection.transmit_rate_mbps} Mbps`} />
                <MetricBox
                    label="Latency"
                    value={latency ? `${latency.avg_ms}ms` : '—'}
                    sub={latency ? `${latency.min_ms}–${latency.max_ms}ms` : ''}
                />
                <MetricBox
                    label="Throughput"
                    value={throughput?.total_mbps !== undefined ? `${throughput.total_mbps} Mbps` : '—'}
                    sub={throughput ? `↓${throughput.download_mbps} ↑${throughput.upload_mbps}` : ''}
                />
                <MetricBox
                    label="WMCDA Score"
                    value={score ? `${(score * 100).toFixed(1)}%` : '—'}
                    accent
                />
            </div>
        </div>
    );
}

function MetricBox({ label, value, sub, accent }) {
    return (
        <div style={{
            padding: '12px 14px',
            background: 'var(--bg-glass)',
            border: '1px solid var(--border-subtle)',
            borderRadius: 'var(--radius-sm)',
        }}>
            <div style={{
                fontSize: '0.68rem',
                color: 'var(--text-muted)',
                textTransform: 'uppercase',
                letterSpacing: '0.06em',
                marginBottom: '4px',
            }}>
                {label}
            </div>
            <div style={{
                fontSize: accent ? '1rem' : '0.9rem',
                fontWeight: 700,
                fontFamily: "'JetBrains Mono', monospace",
                color: accent ? 'var(--accent-cyan)' : 'var(--text-primary)',
                wordBreak: 'break-all',
            }}>
                {value}
            </div>
            {sub && (
                <div style={{
                    fontSize: '0.65rem',
                    color: 'var(--text-muted)',
                    marginTop: '2px',
                }}>
                    {sub}
                </div>
            )}
        </div>
    );
}
