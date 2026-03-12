export default function Header({ scanCount, lastScan }) {
    const formatTime = (iso) => {
        if (!iso) return '—';
        const d = new Date(iso);
        return d.toLocaleTimeString('en-IN', { hour: '2-digit', minute: '2-digit', second: '2-digit' });
    };

    return (
        <header className="header">
            <div className="header-brand">
                <div className="header-logo">⚡</div>
                <div>
                    <div className="header-title">Adaptive Network Switching</div>
                    <div className="header-subtitle">Next-Gen Intelligent Network Selection</div>
                </div>
            </div>
            <div className="header-status">
                <div className="status-indicator">
                    <span className="status-dot" />
                    System Online
                </div>
                <div className="status-indicator">
                    🔍 Scans: {scanCount}
                </div>
                <div className="status-indicator">
                    🕐 Last: {formatTime(lastScan)}
                </div>
            </div>
        </header>
    );
}
