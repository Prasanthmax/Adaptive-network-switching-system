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

const COLORS = ['#2872A1', '#10B981', '#8B5CF6', '#F59E0B', '#EF4444'];
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
                    Network Comparison
                </div>
                <span className="card-badge">Top {networks.length}</span>
            </div>
            <div className="chart-container">
                <ResponsiveContainer width="100%" height={320}>
                    <RadarChart data={data} cx="50%" cy="50%" outerRadius="72%">
                        <PolarGrid stroke="rgba(40, 114, 161, 0.15)" />
                        <PolarAngleAxis
                            dataKey="metric"
                            tick={{ fill: '#334155', fontSize: 11, fontWeight: 600 }}
                        />
                        <PolarRadiusAxis
                            angle={30}
                            domain={[0, 100]}
                            tick={{ fill: '#64748B', fontSize: 9, fontWeight: 500 }}
                            tickCount={5}
                        />
                        {networks.map((net, i) => (
                            <Radar
                                key={net.ssid}
                                name={net.ssid}
                                dataKey={net.ssid}
                                stroke={COLORS[i % COLORS.length]}
                                fill={COLORS[i % COLORS.length]}
                                fillOpacity={i === 0 ? 0.15 : 0.03}
                                strokeWidth={i === 0 ? 2.5 : 1.5}
                            />
                        ))}
                        <Tooltip
                            contentStyle={{
                                backgroundColor: '#FFFFFF',
                                border: '1px solid rgba(40, 114, 161, 0.2)',
                                borderRadius: '12px',
                                color: '#1C4F70',
                                fontSize: '12px',
                                fontFamily: 'Outfit, sans-serif',
                                boxShadow: '0 4px 20px rgba(0, 0, 0, 0.05)',
                            }}
                            formatter={(value) => `${value}%`}
                        />
                        <Legend wrapperStyle={{ fontSize: '11px', color: '#334155' }} />
                    </RadarChart>
                </ResponsiveContainer>
            </div>
        </div>
    );
}
