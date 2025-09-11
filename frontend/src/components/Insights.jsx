import React, { useState } from 'react';
import './Insights.css';

function Insights({ analysis }) {
    const [activeTab, setActiveTab] = useState('insights');

    if (!analysis || !analysis.ai_insights) {
        return (
            <div className="insights-container">
                <p>No insights available</p>
            </div>
        );
    }

    const { ai_insights, recommendations } = analysis;

    const renderInsightsList = (insights) => {
        if (!insights || insights.length === 0) return <p>No insights available</p>;
        
        return (
            <ul className="insights-list">
                {insights.map((insight, index) => (
                    <li key={index} className="insight-item">
                        <span className="insight-text" dangerouslySetInnerHTML={{ __html: insight }} />
                    </li>
                ))}
            </ul>
        );
    };

    const renderRecommendationsList = (recs) => {
        if (!recs || recs.length === 0) return <p>No recommendations available</p>;
        
        return (
            <ul className="recommendations-list">
                {recs.map((rec, index) => (
                    <li key={index} className="recommendation-item">
                        <span className="recommendation-text">{rec}</span>
                    </li>
                ))}
            </ul>
        );
    };

    const tabs = [
        { id: 'insights', label: '🧠 AI Insights', icon: '🔍' },
        { id: 'recommendations', label: '💡 Recommendations', icon: '🎯' },
        { id: 'risks', label: '⚠️ Risk Analysis', icon: '🛡️' }
    ];

    return (
        <div className="insights-container">
            <div className="insights-header">
                <h3>🤖 AI-Powered Financial Intelligence</h3>
                <p>Advanced analysis powered by machine learning algorithms</p>
            </div>

            <div className="insights-tabs">
                {tabs.map(tab => (
                    <button
                        key={tab.id}
                        className={`tab-button ${activeTab === tab.id ? 'active' : ''}`}
                        onClick={() => setActiveTab(tab.id)}
                    >
                        <span className="tab-icon">{tab.icon}</span>
                        <span className="tab-label">{tab.label}</span>
                    </button>
                ))}
            </div>

            <div className="insights-content">
                {activeTab === 'insights' && (
                    <div className="insights-tab">
                        <div className="insights-grid">
                            <div className="insight-category">
                                <h4>💰 Cash Flow Analysis</h4>
                                {renderInsightsList(ai_insights.cash_flow_insights)}
                            </div>

                            <div className="insight-category">
                                <h4>📊 Profitability Analysis</h4>
                                {renderInsightsList(ai_insights.profitability_insights)}
                            </div>

                            <div className="insight-category">
                                <h4>📈 Trend Analysis</h4>
                                {renderInsightsList(ai_insights.trend_insights)}
                            </div>

                            <div className="insight-category">
                                <h4>🏥 Financial Health</h4>
                                {renderInsightsList(ai_insights.health_insights)}
                            </div>

                            {ai_insights.growth_opportunities && ai_insights.growth_opportunities.length > 0 && (
                                <div className="insight-category opportunities">
                                    <h4>🚀 Growth Opportunities</h4>
                                    <div className="opportunities-grid">
                                        {ai_insights.growth_opportunities.map((opportunity, index) => (
                                            <div key={index} className="opportunity-card">
                                                <div className="opportunity-header">
                                                    <span className="opportunity-type">{opportunity.type?.toUpperCase()}</span>
                                                    <span className="opportunity-timeline">{opportunity.timeline}</span>
                                                </div>
                                                <div className="opportunity-description">{opportunity.description}</div>
                                                <div className="opportunity-potential">{opportunity.potential}</div>
                                            </div>
                                        ))}
                                    </div>
                                </div>
                            )}
                        </div>
                    </div>
                )}

                {activeTab === 'recommendations' && (
                    <div className="recommendations-tab">
                        <div className="recommendations-grid">
                            {recommendations.immediate_actions && recommendations.immediate_actions.length > 0 && (
                                <div className="recommendation-category urgent">
                                    <h4>🔥 Immediate Actions Required</h4>
                                    <div className="urgency-badge">Take action within 24-48 hours</div>
                                    {renderRecommendationsList(recommendations.immediate_actions)}
                                </div>
                            )}

                            {recommendations.short_term_strategies && recommendations.short_term_strategies.length > 0 && (
                                <div className="recommendation-category short-term">
                                    <h4>⚡ Short-term Strategies (1-3 months)</h4>
                                    {renderRecommendationsList(recommendations.short_term_strategies)}
                                </div>
                            )}

                            {recommendations.cost_optimization && recommendations.cost_optimization.length > 0 && (
                                <div className="recommendation-category cost">
                                    <h4>💰 Cost Optimization</h4>
                                    {renderRecommendationsList(recommendations.cost_optimization)}
                                </div>
                            )}

                            {recommendations.revenue_enhancement && recommendations.revenue_enhancement.length > 0 && (
                                <div className="recommendation-category revenue">
                                    <h4>📈 Revenue Enhancement</h4>
                                    {renderRecommendationsList(recommendations.revenue_enhancement)}
                                </div>
                            )}

                            {recommendations.long_term_strategies && recommendations.long_term_strategies.length > 0 && (
                                <div className="recommendation-category long-term">
                                    <h4>🎯 Long-term Strategic Initiatives</h4>
                                    {renderRecommendationsList(recommendations.long_term_strategies)}
                                </div>
                            )}

                            {recommendations.strategic_recommendations && recommendations.strategic_recommendations.length > 0 && (
                                <div className="recommendation-category strategic">
                                    <h4>🧭 Strategic Recommendations</h4>
                                    {renderRecommendationsList(recommendations.strategic_recommendations)}
                                </div>
                            )}
                        </div>
                    </div>
                )}

                {activeTab === 'risks' && (
                    <div className="risks-tab">
                        {ai_insights.risk_assessment && ai_insights.risk_assessment.length > 0 ? (
                            <div className="risks-grid">
                                {ai_insights.risk_assessment.map((risk, index) => (
                                    <div key={index} className={`risk-card ${risk.level}`}>
                                        <div className="risk-header">
                                            <span className={`risk-level ${risk.level}`}>
                                                {risk.level?.toUpperCase()} RISK
                                            </span>
                                            <span className="risk-type">{risk.type?.toUpperCase()}</span>
                                        </div>
                                        <div className="risk-description">{risk.description}</div>
                                        <div className="risk-mitigation">
                                            <strong>Mitigation Strategy:</strong>
                                            <p>{risk.mitigation}</p>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        ) : (
                            <div className="no-risks">
                                <div className="no-risks-icon">✅</div>
                                <h4>No Major Risks Detected</h4>
                                <p>Your financial data doesn't show any immediate red flags. Continue monitoring your key metrics to maintain this healthy status.</p>
                            </div>
                        )}
                        
                        {recommendations.risk_mitigation && recommendations.risk_mitigation.length > 0 && (
                            <div className="risk-mitigation-section">
                                <h4>🛡️ Risk Mitigation Strategies</h4>
                                {renderRecommendationsList(recommendations.risk_mitigation)}
                            </div>
                        )}
                    </div>
                )}
            </div>

            {/* Summary Footer */}
            <div className="insights-footer">
                <div className="ai-powered-badge">
                    <span className="ai-icon">🤖</span>
                    <span>Powered by Advanced AI & Machine Learning</span>
                </div>
                <div className="analysis-confidence">
                    <span>Analysis based on {analysis.data_quality?.rows_processed || 0} transactions</span>
                </div>
            </div>
        </div>
    );
}

export default Insights;
