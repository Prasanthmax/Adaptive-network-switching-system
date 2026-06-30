export default function Header({ scanCount, lastScan, onMenuToggle, menuOpen }) {
    const formatTime = (iso) => {
        if (!iso) return '—';
        const d = new Date(iso);
        return d.toLocaleTimeString('en-IN', { hour: '2-digit', minute: '2-digit', second: '2-digit' });
    };

    return (
        <header className="header">
            <div className="header-brand">
                <div className="header-logo" style={{ fontSize: '14px', letterSpacing: '0.5px' }}>ANS</div>
                <div>
                    <div className="header-title">Adaptive Network Switching</div>
                    <div className="header-subtitle">Intelligent Network Selection Engine</div>
                </div>
            </div>
            <div className="header-actions">
                <div className="header-status">
                    <div className="status-indicator">
                        <span className="status-dot" />
                        Online
                    </div>
                    <div className="status-indicator">
                        Scans: {scanCount}
                    </div>
                    <div className="status-indicator">
                        Last: {formatTime(lastScan)}
                    </div>
                </div>
                <button
                    className={`menu-toggle-btn ${menuOpen ? 'open' : ''}`}
                    onClick={onMenuToggle}
                >
                    {menuOpen ? 'Close' : 'Formula & Weights'}
                </button>
            </div>
        </header>
    );
}
