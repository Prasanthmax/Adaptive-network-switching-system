import {
    RadarChart,
    Radar,
    PolarGrid,
    PolarAngleAxis,
    PolarRadiusAxis,
    ResponsiveContainer,
    Tooltip,
    Legend,
} from 'recharts';

const COLORS = ['#6366f1', '#22d3ee', '#10b981', '#f59e0b', '#f43f5e'];
const METRIC_LABELS = {
    signal_strength: 'Signal',
    bandwidth: 'Bandwidth',
    latency: 'Latency',
    reliability: 'Reliability',
    security: 'Security',
    cost_efficiency: 'Cost Eff.',
};

export default function RadarChartCard({ networks }) {
    if (!networks || networks.length === 0) return null;

    const metrics = Object.keys(METRIC_LABELS);
    const data = metrics.map((metric) => {
        const point = { metric: METRIC_LABELS[metric] };
        networks.forEach((net) => {
            const normVal = net.normalized_metrics?.[metric] || 0;
            point[net.ssid] = Math.round(normVal * 100);
        });
        return point;
    });

    return (
        <div className="glass-card animate-in delay-4">
            <div className="card-header">
                <div className="card-title">
                    <span className="icon">🎯</span>
                    Network Comparison
                </div>
                <span className="card-badge">Top {networks.length}</span>
            </div>
            <div className="chart-container">
                <ResponsiveContainer width="100%" height={340}>
                    <RadarChart data={data} cx="50%" cy="50%" outerRadius="72%">
                        <PolarGrid stroke="rgba(255,255,255,0.08)" />
                        <PolarAngleAxis
                            dataKey="metric"
                            tick={{ fill: '#94a3b8', fontSize: 11, fontWeight: 500 }}
                        />
                        <PolarRadiusAxis
                            angle={30}
                            domain={[0, 100]}
                            tick={{ fill: '#64748b', fontSize: 9 }}
                            tickCount={5}
                        />
                        {networks.map((net, i) => (
                            <Radar
                                key={net.ssid}
                                name={net.ssid}
                                dataKey={net.ssid}
                                stroke={COLORS[i % COLORS.length]}
                                fill={COLORS[i % COLORS.length]}
                                fillOpacity={i === 0 ? 0.2 : 0.05}
                                strokeWidth={i === 0 ? 2.5 : 1.5}
                            />
                        ))}
                        <Tooltip
                            contentStyle={{
                                backgroundColor: 'rgba(17, 24, 39, 0.95)',
                                border: '1px solid rgba(255,255,255,0.1)',
                                borderRadius: '8px',
                                color: '#f1f5f9',
                                fontSize: '12px',
                            }}
                            formatter={(value) => `${value}%`}
                        />
                        <Legend wrapperStyle={{ fontSize: '11px', color: '#94a3b8' }} />
                    </RadarChart>
                </ResponsiveContainer>
            </div>
        </div>
    );
}
