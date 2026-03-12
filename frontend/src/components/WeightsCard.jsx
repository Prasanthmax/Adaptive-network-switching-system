const METRIC_LABELS = {
    signal_strength: 'Signal',
    bandwidth: 'Bandwidth',
    latency: 'Latency',
    reliability: 'Reliability',
    security: 'Security',
    cost: 'Cost',
};

const METRIC_COLORS = {
    signal_strength: '#6366f1',
    bandwidth: '#22d3ee',
    latency: '#10b981',
    reliability: '#f59e0b',
    security: '#8b5cf6',
    cost: '#f43f5e',
};

export default function WeightsCard({ weights }) {
    if (!weights) return null;

    const maxWeight = Math.max(...Object.values(weights));

    return (
        <div className="glass-card animate-in delay-6">
            <div className="card-header">
                <div className="card-title">
                    <span className="icon">⚖️</span>
                    Weight Distribution
                </div>
                <span className="card-badge">Profile</span>
            </div>
            <div className="card-body">
                <div className="weights-grid">
                    {Object.entries(weights).map(([key, value]) => (
                        <div key={key} className="weight-item">
                            <div className="weight-name">{METRIC_LABELS[key] || key}</div>
                            <div
                                className="weight-value"
                                style={{ color: METRIC_COLORS[key] || 'var(--text-primary)' }}
                            >
                                {(value * 100).toFixed(0)}%
                            </div>
                            <div className="weight-bar">
                                <div
                                    className="weight-bar-fill"
                                    style={{
                                        width: `${(value / maxWeight) * 100}%`,
                                        background: METRIC_COLORS[key] || 'var(--accent-primary)',
                                    }}
                                />
                            </div>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
}
