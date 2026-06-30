const METRIC_LABELS = {
    signal_strength: 'Signal',
    bandwidth: 'Bandwidth',
    latency: 'Latency',
    reliability: 'Reliability',
    security: 'Security',
    cost: 'Cost',
    cost_efficiency: 'Cost',
};

const METRIC_COLORS = {
    signal_strength: '#8B5CF6',   /* violet */
    bandwidth: '#2872A1',         /* Ocean Blue */
    latency: '#10B981',           /* emerald */
    reliability: '#F59E0B',       /* amber */
    security: '#6366F1',           /* indigo */
    cost: '#EF4444',              /* rose */
    cost_efficiency: '#EF4444',
};

export default function WeightsCard({ weights }) {
    if (!weights) return null;

    const maxWeight = Math.max(...Object.values(weights));

    return (
        <div className="glass-card animate-in delay-6">
            <div className="card-header">
                <div className="card-title">
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
                                        background: METRIC_COLORS[key] || 'var(--ocean-blue)',
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
