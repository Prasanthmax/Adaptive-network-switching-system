import { useState } from 'react';

const GEN_CLASSES = {
    'WiFi 6': 'type-wifi6',
    'WiFi 6E': 'type-wifi6e',
    'WiFi 5': 'type-wifi5',
    'WiFi 4': 'type-4g',
    'WiFi 3': 'type-3g',
    'WiFi 7': 'type-5g',
};

function getScoreClass(score) {
    if (score >= 0.85) return 'excellent';
    if (score >= 0.70) return 'good';
    if (score >= 0.55) return 'adequate';
    if (score >= 0.40) return 'below';
    return 'poor';
}

export default function NetworkList({ networks, onSwitch }) {
    const [switching, setSwitching] = useState(null);

    const handleSwitch = async (ssid) => {
        if (!onSwitch) return;
        setSwitching(ssid);
        await onSwitch(ssid);
        setSwitching(null);
    };

    if (!networks || networks.length === 0) {
        return (
            <div className="glass-card">
                <div className="card-header">
                    <div className="card-title">
                        <span className="icon">📊</span>
                        Network Rankings
                    </div>
                </div>
                <div className="empty-state">
                    <div className="empty-icon">📵</div>
                    <div className="empty-title">No networks found</div>
                    <div className="empty-desc">Run a scan to discover real WiFi networks.</div>
                </div>
            </div>
        );
    }

    return (
        <div className="glass-card">
            <div className="card-header">
                <div className="card-title">
                    <span className="icon">📊</span>
                    Real Network Rankings — WMCDA Scored
                </div>
                <span className="card-badge">{networks.length} networks</span>
            </div>
            <div className="card-body">
                <div className="network-list">
                    {networks.map((net, i) => {
                        const tier = getScoreClass(net.composite_score);
                        const isBest = net.rank === 1;
                        const genClass = GEN_CLASSES[net.generation] || 'type-3g';

                        return (
                            <div
                                key={net.bssid || net.ssid}
                                className={`network-item ${isBest ? 'best' : ''} ${net.is_current ? 'current' : ''} animate-in delay-${Math.min(i + 1, 10)}`}
                                style={{ gridTemplateColumns: '40px 1fr 90px 90px 90px' }}
                            >
                                <div className="network-rank">{net.rank}</div>

                                <div className="network-info">
                                    <div className="network-name">
                                        {net.is_current && '🔗 '}
                                        {isBest && !net.is_current && '👑 '}
                                        {net.ssid}
                                        {net.is_known && (
                                            <span style={{
                                                fontSize: '0.6rem',
                                                background: 'rgba(99, 102, 241, 0.15)',
                                                color: '#a5b4fc',
                                                padding: '1px 6px',
                                                borderRadius: '4px',
                                                marginLeft: '8px',
                                            }}>saved</span>
                                        )}
                                    </div>
                                    <div className="network-meta">
                                        <span>📶 {net.signal_percent}%</span>
                                        <span>📻 {net.band}</span>
                                        <span>⏱ {net.latency_ms}ms</span>
                                        <span>🔒 {net.authentication}</span>
                                    </div>
                                </div>

                                <div className={`network-type-badge ${genClass}`}>
                                    {net.generation || net.radio_type}
                                </div>

                                <div className="network-score">
                                    <div className={`score-value score-${tier}`}>
                                        {(net.composite_score * 100).toFixed(1)}%
                                    </div>
                                    <div className="score-bar-container">
                                        <div
                                            className={`score-bar bar-${tier}`}
                                            style={{ width: `${net.composite_score * 100}%` }}
                                        />
                                    </div>
                                </div>

                                <div style={{ textAlign: 'center' }}>
                                    {net.is_current ? (
                                        <span style={{
                                            fontSize: '0.7rem',
                                            color: '#6ee7b7',
                                            fontWeight: 600,
                                        }}>Connected</span>
                                    ) : net.is_known ? (
                                        <button
                                            onClick={() => handleSwitch(net.ssid)}
                                            disabled={switching === net.ssid}
                                            style={{
                                                padding: '5px 12px',
                                                fontSize: '0.7rem',
                                                fontWeight: 600,
                                                fontFamily: 'inherit',
                                                background: 'var(--gradient-primary)',
                                                color: 'white',
                                                border: 'none',
                                                borderRadius: 'var(--radius-full)',
                                                cursor: 'pointer',
                                                opacity: switching === net.ssid ? 0.5 : 1,
                                            }}
                                        >
                                            {switching === net.ssid ? '...' : 'Switch'}
                                        </button>
                                    ) : (
                                        <span style={{
                                            fontSize: '0.65rem',
                                            color: 'var(--text-muted)',
                                        }}>Unknown</span>
                                    )}
                                </div>
                            </div>
                        );
                    })}
                </div>
            </div>
        </div>
    );
}
