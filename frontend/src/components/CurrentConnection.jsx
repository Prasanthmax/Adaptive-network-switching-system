/**
 * CurrentConnection — Shows the currently connected WiFi with live metrics.
 */
export default function CurrentConnection({ connection, score, latency, throughput }) {
    if (!connection) return null;

    return (
        <div className="glass-card current-connection animate-in delay-2" style={{ marginBottom: '20px' }}>
            <div className="card-header">
                <div className="card-title">
                    Currently Connected
                    <span className="live-dot" />
                </div>
                <span className="card-badge" style={{
                    background: 'var(--accent-emerald-dim)',
                    color: 'var(--accent-emerald)',
                    borderColor: 'rgba(74, 222, 128, 0.25)',
                }}>
                    LIVE
                </span>
            </div>
            <div className="card-body" style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(130px, 1fr))', gap: '10px' }}>
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
            padding: '10px 12px',
            background: 'var(--bg-card)',
            border: '1px solid var(--border-default)',
            borderRadius: 'var(--radius-sm)',
        }}>
            <div style={{
                fontSize: '0.62rem',
                color: 'var(--text-muted)',
                textTransform: 'uppercase',
                letterSpacing: '0.06em',
                marginBottom: '3px',
                fontWeight: 600,
            }}>
                {label}
            </div>
            <div style={{
                fontSize: accent ? '0.95rem' : '0.85rem',
                fontWeight: 700,
                fontFamily: "'JetBrains Mono', monospace",
                color: accent ? 'var(--gold)' : 'var(--text-primary)',
                wordBreak: 'break-all',
            }}>
                {value}
            </div>
            {sub && (
                <div style={{
                    fontSize: '0.6rem',
                    color: 'var(--text-muted)',
                    marginTop: '2px',
                    fontWeight: 500,
                }}>
                    {sub}
                </div>
            )}
        </div>
    );
}
