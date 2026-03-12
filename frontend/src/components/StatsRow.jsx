export default function StatsRow({ totalNetworks, availableNetworks, bestScore, bestName, profile, latency, throughput }) {
    const profileLabels = {
        balanced: '⚖️ Balanced',
        streaming: '🎬 Streaming',
        gaming: '🎮 Gaming',
        enterprise: '🏢 Enterprise',
        cost_sensitive: '💰 Budget',
        iot: '📟 IoT',
    };

    return (
        <div className="stats-row">
            <div className="stat-card purple animate-in delay-1">
                <div className="stat-label">Networks Visible</div>
                <div className="stat-value purple">{totalNetworks}</div>
                <div className="stat-sub">Real WiFi networks detected</div>
            </div>
            <div className="stat-card cyan animate-in delay-2">
                <div className="stat-label">Best Score</div>
                <div className="stat-value cyan">
                    {bestScore ? (bestScore * 100).toFixed(1) + '%' : '—'}
                </div>
                <div className="stat-sub">{bestName || 'No network scored'}</div>
            </div>
            <div className="stat-card emerald animate-in delay-3">
                <div className="stat-label">Latency</div>
                <div className="stat-value emerald">
                    {latency ? latency.avg_ms + 'ms' : '—'}
                </div>
                <div className="stat-sub">
                    {latency ? `Loss: ${latency.packet_loss_percent}%` : 'Ping to 8.8.8.8'}
                </div>
            </div>
            <div className="stat-card warm animate-in delay-4">
                <div className="stat-label">Throughput</div>
                <div className="stat-value warm" style={{ fontSize: '1.3rem' }}>
                    {throughput?.download_mbps !== undefined
                        ? `↓${throughput.download_mbps} ↑${throughput.upload_mbps}`
                        : '—'}
                </div>
                <div className="stat-sub">Mbps (live psutil)</div>
            </div>
        </div>
    );
}
