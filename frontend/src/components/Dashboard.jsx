import React from 'react';
import Insights from './Insights';
import './Dashboard.css';

function Dashboard({ analysis, isLoading }) {
    if (isLoading) {
        return (
            <div className="dashboard-loading">
                <div className="loading-spinner"></div>
                <p>Analyzing your financial data with AI...</p>
            </div>
        );
    }

    if (!analysis || analysis.error) {
        return (
            <div className="dashboard-error">
                <h3>Analysis Error</h3>
                <p>{analysis?.message || 'Unable to analyze the uploaded data'}</p>
                {analysis?.suggestions && (
                    <div className="error-suggestions">
                        <h4>Suggestions:</h4>
                        <ul>
                            {analysis.suggestions.map((suggestion, index) => (
                                <li key={index}>{suggestion}</li>
                            ))}
                        </ul>
                    </div>
                )}
            </div>
        );
    }

    const { financial_metrics, benchmark_analysis, executive_summary, data_quality } = analysis;
    const { cash_flow, profitability, health_score, trend_analysis } = financial_metrics;

    return (
        <div className="dashboard">
            <div className="dashboard-header">
                <h2>AI CFO Financial Dashboard</h2>
                <div className="file-info">
                    <span>📊 {analysis.file_processed}</span>
                    <span>📅 {new Date(analysis.timestamp).toLocaleDateString()}</span>
                    <span>📈 {data_quality.rows_processed} transactions analyzed</span>
                </div>
            </div>

            {/* Financial Health Score - Prominent Display */}
            <div className="health-score-card">
                <div className="score-circle">
                    <div className="score-value">{health_score.score}</div>
                    <div className="score-label">Health Score</div>
                </div>
                <div className="score-details">
                    <div className="grade">Grade: {health_score.grade}</div>
                    <div className="assessment">{health_score.assessment}</div>
                </div>
            </div>

            {/* Key Metrics Grid */}
            <div className="metrics-grid">
                <div className="metric-card cash-flow">
                    <div className="metric-header">
                        <h3>💰 Cash Flow</h3>
                        <span className={`status ${cash_flow.net_cash_flow >= 0 ? 'positive' : 'negative'}`}>
                            {cash_flow.net_cash_flow >= 0 ? '📈' : '📉'}
                        </span>
                    </div>
                    <div className="metric-value">
                        ${cash_flow.net_cash_flow?.toLocaleString() || '0'}
                    </div>
                    <div className="metric-details">
                        <div>Income: ${cash_flow.total_income?.toLocaleString() || '0'}</div>
                        <div>Expenses: ${cash_flow.total_expenses?.toLocaleString() || '0'}</div>
                        <div>Monthly Avg: ${cash_flow.monthly_average?.toLocaleString() || '0'}</div>
                    </div>
                </div>

                <div className="metric-card profitability">
                    <div className="metric-header">
                        <h3>📊 Profitability</h3>
                        <span className={`status ${profitability.gross_profit_margin >= 0.1 ? 'good' : 'warning'}`}>
                            {profitability.gross_profit_margin >= 0.1 ? '✅' : '⚠️'}
                        </span>
                    </div>
                    <div className="metric-value">
                        {(profitability.gross_profit_margin * 100)?.toFixed(1) || '0'}%
                    </div>
                    <div className="metric-details">
                        <div>Revenue: ${profitability.revenue?.toLocaleString() || '0'}</div>
                        <div>Gross Profit: ${profitability.gross_profit?.toLocaleString() || '0'}</div>
                        <div>Per Transaction: ${profitability.profit_per_transaction?.toFixed(2) || '0'}</div>
                    </div>
                </div>

                <div className="metric-card trend">
                    <div className="metric-header">
                        <h3>📈 Trend Analysis</h3>
                        <span className={`status ${trend_analysis.trend_slope >= 0 ? 'positive' : 'negative'}`}>
                            {trend_analysis.current_trajectory === 'improving' ? '🚀' : '📉'}
                        </span>
                    </div>
                    <div className="metric-value">
                        {trend_analysis.current_trajectory || 'Stable'}
                    </div>
                    <div className="metric-details">
                        <div>Trend Strength: {(trend_analysis.trend_strength * 100)?.toFixed(0) || '0'}%</div>
                        <div>R-Squared: {(trend_analysis.r_squared * 100)?.toFixed(0) || '0'}%</div>
                        <div>Volatility: ${trend_analysis.volatility?.toLocaleString() || '0'}</div>
                    </div>
                </div>
            </div>

            {/* Executive Summary */}
            {executive_summary && (
                <div className="executive-summary">
                    <h3>🎯 Executive Summary</h3>
                    <div className="summary-grid">
                        <div className="summary-item">
                            <h4>Overall Health</h4>
                            <span className="health-grade">{executive_summary.overall_health}</span>
                        </div>
                        <div className="summary-item">
                            <h4>Key Findings</h4>
                            <ul>
                                {executive_summary.key_findings?.map((finding, index) => (
                                    <li key={index}>{finding}</li>
                                ))}
                            </ul>
                        </div>
                        <div className="summary-item">
                            <h4>Critical Issues</h4>
                            <ul>
                                {executive_summary.critical_issues?.map((issue, index) => (
                                    <li key={index} className="critical">{issue}</li>
                                ))}
                            </ul>
                        </div>
                        <div className="summary-item">
                            <h4>Opportunities</h4>
                            <ul>
                                {executive_summary.opportunities?.map((opportunity, index) => (
                                    <li key={index} className="opportunity">{opportunity}</li>
                                ))}
                            </ul>
                        </div>
                    </div>
                </div>
            )}

            {/* Industry Benchmarking */}
            {benchmark_analysis && Object.keys(benchmark_analysis).length > 0 && (
                <div className="benchmark-analysis">
                    <h3>🏆 Industry Benchmarking</h3>
                    <div className="benchmark-grid">
                        {Object.entries(benchmark_analysis).map(([metric, data]) => (
                            <div key={metric} className="benchmark-item">
                                <h4>{metric.replace('_', ' ').toUpperCase()}</h4>
                                <div className="benchmark-comparison">
                                    <div className="your-performance">
                                        <span>Your Performance</span>
                                        <strong>{(data.your_performance * 100).toFixed(1)}%</strong>
                                    </div>
                                    <div className="industry-benchmark">
                                        <span>Industry Average</span>
                                        <strong>{(data.industry_benchmark * 100).toFixed(1)}%</strong>
                                    </div>
                                    <div className={`performance-indicator ${data.performance}`}>
                                        {data.performance === 'above' ? '📈 Above Average' : '📉 Below Average'}
                                        <span className="percentile">({data.percentile}th percentile)</span>
                                    </div>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            )}

            {/* Alerts Section */}
            {analysis.alerts && (
                <div className="alerts-section">
                    <h3>🚨 Financial Alerts</h3>
                    <div className="alerts-grid">
                        {analysis.alerts.critical_alerts?.length > 0 && (
                            <div className="alert-group critical">
                                <h4>Critical Alerts</h4>
                                {analysis.alerts.critical_alerts.map((alert, index) => (
                                    <div key={index} className="alert-item">
                                        <span className="alert-icon">🔴</span>
                                        <div className="alert-content">
                                            <strong>{alert.message}</strong>
                                            <small>Urgency: {alert.urgency}</small>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        )}
                        
                        {analysis.alerts.warning_alerts?.length > 0 && (
                            <div className="alert-group warning">
                                <h4>Warning Alerts</h4>
                                {analysis.alerts.warning_alerts.map((alert, index) => (
                                    <div key={index} className="alert-item">
                                        <span className="alert-icon">⚠️</span>
                                        <div className="alert-content">
                                            <strong>{alert.message}</strong>
                                            <small>Urgency: {alert.urgency}</small>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        )}

                        {analysis.alerts.opportunity_alerts?.length > 0 && (
                            <div className="alert-group opportunity">
                                <h4>Opportunities</h4>
                                {analysis.alerts.opportunity_alerts.map((alert, index) => (
                                    <div key={index} className="alert-item">
                                        <span className="alert-icon">💡</span>
                                        <div className="alert-content">
                                            <strong>{alert.message}</strong>
                                            <small>Impact: {alert.impact}</small>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        )}
                    </div>
                </div>
            )}

            {/* Forecast Section */}
            {analysis.forecast && !analysis.forecast.error && (
                <div className="forecast-section">
                    <h3>🔮 6-Month Forecast</h3>
                    <div className="forecast-content">
                        <div className="confidence-level">
                            Confidence Level: <span className={`confidence ${analysis.forecast.confidence_level}`}>
                                {analysis.forecast.confidence_level.toUpperCase()}
                            </span>
                        </div>
                        <div className="scenario-analysis">
                            <h4>Scenario Analysis (Average Monthly Cash Flow)</h4>
                            <div className="scenarios">
                                <div className="scenario optimistic">
                                    <span>📈 Optimistic</span>
                                    <strong>${(analysis.forecast.scenario_analysis.optimistic.reduce((a, b) => a + b, 0) / 6).toLocaleString()}</strong>
                                </div>
                                <div className="scenario realistic">
                                    <span>🎯 Realistic</span>
                                    <strong>${(analysis.forecast.scenario_analysis.realistic.reduce((a, b) => a + b, 0) / 6).toLocaleString()}</strong>
                                </div>
                                <div className="scenario pessimistic">
                                    <span>📉 Pessimistic</span>
                                    <strong>${(analysis.forecast.scenario_analysis.pessimistic.reduce((a, b) => a + b, 0) / 6).toLocaleString()}</strong>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            )}

            {/* AI Insights and Recommendations */}
            <Insights analysis={analysis} />

            {/* Action Items */}
            {analysis.action_items && analysis.action_items.length > 0 && (
                <div className="action-items">
                    <h3>✅ Action Items</h3>
                    <div className="action-grid">
                        {['high', 'medium', 'low'].map(priority => {
                            const items = analysis.action_items.filter(item => item.priority === priority);
                            if (items.length === 0) return null;
                            
                            return (
                                <div key={priority} className={`action-group ${priority}`}>
                                    <h4>{priority.toUpperCase()} Priority</h4>
                                    {items.map((item, index) => (
                                        <div key={index} className="action-item">
                                            <div className="action-content">
                                                <strong>{item.action}</strong>
                                                <div className="action-meta">
                                                    <span>Category: {item.category}</span>
                                                    <span>Timeline: {item.timeline}</span>
                                                </div>
                                            </div>
                                        </div>
                                    ))}
                                </div>
                            );
                        })}
                    </div>
                </div>
            )}

            {/* Data Quality Info */}
            <div className="data-quality">
                <h3>📋 Data Quality Report</h3>
                <div className="quality-metrics">
                    <div>Completeness: {data_quality.completeness_score?.toFixed(1)}%</div>
                    <div>Period: {data_quality.date_range?.period_months?.toFixed(1)} months</div>
                    <div>Columns: {data_quality.columns_found?.join(', ')}</div>
                </div>
            </div>
        </div>
    );
}

export default Dashboard;
