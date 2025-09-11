import React, { useState } from 'react';
import FileUpload from './components/FileUpload';
import Dashboard from './components/Dashboard';
import './App.css';

function App() {
    const [analysis, setAnalysis] = useState(null);
    const [isLoading, setIsLoading] = useState(false);

    const handleAnalysis = (analysisResult) => {
        setAnalysis(analysisResult);
        setIsLoading(false);
    };

    const handleLoading = (loading) => {
        setIsLoading(loading);
    };

    const resetAnalysis = () => {
        setAnalysis(null);
        setIsLoading(false);
    };

    return (
        <div className="App">
            <header className="app-header">
                <div className="header-content">
                    <h1>🤖 Nib AI</h1>
                    <p>Intelligent Financial Analysis for Smart Business Decisions</p>
                    {analysis && !isLoading && (
                        <button className="new-analysis-btn" onClick={resetAnalysis}>
                            📊 Analyze New Data
                        </button>
                    )}
                </div>
            </header>

            <main className="app-main">
                {!analysis && !isLoading ? (
                    <FileUpload onAnalysis={handleAnalysis} onLoading={handleLoading} />
                ) : (
                    <Dashboard analysis={analysis} isLoading={isLoading} />
                )}
            </main>

            <footer className="app-footer">
                <div className="footer-content">
                    <div className="footer-section">
                        <h4>🚀 AI-Powered Features</h4>
                        <ul>
                            <li>Advanced Cash Flow Analysis</li>
                            <li>Profitability Intelligence</li>
                            <li>Risk Detection & Mitigation</li>
                            <li>Industry Benchmarking</li>
                        </ul>
                    </div>
                    <div className="footer-section">
                        <h4>📊 Analytics & Insights</h4>
                        <ul>
                            <li>Real-time Financial Health Score</li>
                            <li>6-Month Cash Flow Forecasting</li>
                            <li>Anomaly Detection</li>
                            <li>Actionable Recommendations</li>
                        </ul>
                    </div>
                    <div className="footer-section">
                        <h4>🔒 Enterprise Grade</h4>
                        <ul>
                            <li>Bank-level Security</li>
                            <li>GDPR Compliant</li>
                            <li>Multi-format Support</li>
                            <li>Export & Integration</li>
                        </ul>
                    </div>
                </div>
                <div className="footer-bottom">
                    <p>&copy; 2024 AI CFO. Empowering businesses with intelligent financial insights.</p>
                    <div className="footer-badges">
                        <span className="badge">✨ AI Powered</span>
                        <span className="badge">🔒 Secure</span>
                        <span className="badge">📈 Professional</span>
                    </div>
                </div>
            </footer>
        </div>
    );
}

export default App;
