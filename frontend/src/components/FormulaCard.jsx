export default function FormulaCard({ formula }) {
    if (!formula) return null;

    return (
        <div className="glass-card formula-section animate-in delay-5">
            <div className="card-header">
                <div className="card-title">
                    Scoring Formula
                </div>
                <span className="card-badge">WMCDA</span>
            </div>
            <div className="card-body">
                <div className="formula-box">{formula}</div>
            </div>
        </div>
    );
}
