import numpy as np
from datetime import datetime, timedelta

def generate_insights(cash_flow, profitability, cash_flow_trend, health_score):
    """
    Advanced AI-powered insights generation with contextual analysis.
    """
    insights = {
        'cash_flow_insights': _analyze_cash_flow(cash_flow),
        'profitability_insights': _analyze_profitability(profitability),
        'trend_insights': _analyze_trends(cash_flow_trend),
        'health_insights': _analyze_health_score(health_score),
        'risk_assessment': _assess_risks(cash_flow, profitability, cash_flow_trend),
        'growth_opportunities': _identify_opportunities(cash_flow, profitability, cash_flow_trend)
    }
    
    return insights

def generate_recommendations(cash_flow, profitability, cash_flow_trend, benchmark_comparison, business_size):
    """
    Generate AI-powered actionable recommendations based on comprehensive analysis.
    """
    recommendations = {
        'immediate_actions': [],
        'short_term_strategies': [],
        'long_term_strategies': [],
        'strategic_recommendations': [],
        'cost_optimization': [],
        'revenue_enhancement': [],
        'risk_mitigation': []
    }
    
    # Immediate actions based on critical issues
    if cash_flow.get('net_cash_flow', 0) < 0:
        recommendations['immediate_actions'].extend([
            "Immediately review and reduce non-essential expenses",
            "Accelerate accounts receivable collection",
            "Consider emergency financing options if cash position is critical"
        ])
    
    if profitability.get('gross_profit_margin', 0) < 0.05:
        recommendations['immediate_actions'].extend([
            "Conduct urgent pricing analysis and consider price increases",
            "Review and renegotiate supplier contracts",
            "Identify and eliminate unprofitable products/services"
        ])
    
    # Short-term strategies (1-3 months)
    if cash_flow.get('cash_flow_ratio', 1) < 1.2:
        recommendations['short_term_strategies'].extend([
            "Implement stricter payment terms for new customers",
            "Optimize inventory levels to free up working capital",
            "Explore factoring or invoice financing options"
        ])
    
    # Cost optimization
    expense_ratio = cash_flow.get('expense_ratio', 0)
    if expense_ratio > 0.8:
        recommendations['cost_optimization'].extend([
            "Conduct comprehensive expense audit",
            "Implement zero-based budgeting approach",
            "Automate manual processes to reduce labor costs",
            "Negotiate better rates with vendors and suppliers"
        ])
    
    # Revenue enhancement
    if profitability.get('gross_profit_margin', 0) < 0.3:
        recommendations['revenue_enhancement'].extend([
            "Develop premium service offerings with higher margins",
            "Implement value-based pricing strategies",
            "Focus on customer retention to reduce acquisition costs",
            "Explore cross-selling and upselling opportunities"
        ])
    
    # Industry benchmark recommendations
    if benchmark_comparison:
        for metric, data in benchmark_comparison.items():
            if data.get('performance') == 'below':
                if metric == 'profit_margin':
                    recommendations['strategic_recommendations'].append(
                        f"Your profit margin is {data['difference']:.1%} below industry average. "
                        "Focus on operational efficiency and pricing optimization."
                    )
                elif metric == 'cash_flow_ratio':
                    recommendations['strategic_recommendations'].append(
                        f"Your cash flow ratio is below industry standards. "
                        "Improve working capital management and payment collection."
                    )
    
    # Long-term strategies based on trends
    if cash_flow_trend.get('trend_slope', 0) < 0:
        recommendations['long_term_strategies'].extend([
            "Develop new revenue streams to diversify income",
            "Invest in customer acquisition and retention programs",
            "Consider strategic partnerships or market expansion"
        ])
    
    # Business size specific recommendations
    if business_size == 'small':
        recommendations['strategic_recommendations'].extend([
            "Consider cloud-based financial management tools for better insights",
            "Implement automated invoicing and payment systems",
            "Focus on building strong customer relationships for organic growth"
        ])
    
    return recommendations

def create_financial_alerts(cash_flow, profitability, anomalies, health_score):
    """
    Create intelligent financial alerts based on risk analysis.
    """
    alerts = {
        'critical_alerts': [],
        'warning_alerts': [],
        'opportunity_alerts': [],
        'severity_levels': {}
    }
    
    # Critical alerts (immediate attention required)
    if cash_flow.get('net_cash_flow', 0) < -1000:
        alerts['critical_alerts'].append({
            'type': 'cash_flow',
            'message': f"Critical: Negative cash flow of ${abs(cash_flow['net_cash_flow']):,.2f}",
            'impact': 'high',
            'urgency': 'immediate'
        })
    
    if health_score.get('score', 0) < 40:
        alerts['critical_alerts'].append({
            'type': 'financial_health',
            'message': f"Critical: Financial health score is {health_score['score']}/100",
            'impact': 'high',
            'urgency': 'immediate'
        })
    
    # Warning alerts
    if cash_flow.get('cash_flow_ratio', 1) < 1.1:
        alerts['warning_alerts'].append({
            'type': 'liquidity',
            'message': "Warning: Low cash flow ratio indicates potential liquidity issues",
            'impact': 'medium',
            'urgency': 'within_week'
        })
    
    if profitability.get('gross_profit_margin', 0) < 0.1:
        alerts['warning_alerts'].append({
            'type': 'profitability',
            'message': f"Warning: Low profit margin of {profitability['gross_profit_margin']:.1%}",
            'impact': 'medium',
            'urgency': 'within_month'
        })
    
    # Anomaly alerts
    if anomalies.get('anomaly_count', 0) > 0:
        alerts['warning_alerts'].append({
            'type': 'anomalies',
            'message': f"Detected {anomalies['anomaly_count']} unusual transactions worth ${anomalies.get('total_anomaly_value', 0):,.2f}",
            'impact': 'medium',
            'urgency': 'within_week'
        })
    
    # Opportunity alerts
    if cash_flow.get('net_cash_flow', 0) > 10000:
        alerts['opportunity_alerts'].append({
            'type': 'investment',
            'message': f"Opportunity: Strong cash position of ${cash_flow['net_cash_flow']:,.2f} available for investment",
            'impact': 'positive',
            'urgency': 'consider'
        })
    
    if profitability.get('gross_profit_margin', 0) > 0.3:
        alerts['opportunity_alerts'].append({
            'type': 'expansion',
            'message': f"Opportunity: Strong profit margin of {profitability['gross_profit_margin']:.1%} suggests potential for growth",
            'impact': 'positive',
            'urgency': 'consider'
        })
    
    # Calculate severity levels
    alerts['severity_levels'] = {
        'critical': len(alerts['critical_alerts']),
        'warning': len(alerts['warning_alerts']),
        'opportunity': len(alerts['opportunity_alerts']),
        'overall_risk': _calculate_overall_risk(alerts)
    }
    
    return alerts

def _analyze_cash_flow(cash_flow):
    """Detailed cash flow analysis with AI insights."""
    if not cash_flow or 'net_cash_flow' not in cash_flow:
        return ["Unable to analyze cash flow - insufficient data"]
    
    insights = []
    net_cf = cash_flow['net_cash_flow']
    total_income = cash_flow.get('total_income', 0)
    total_expenses = cash_flow.get('total_expenses', 0)
    
    # Cash flow health assessment
    if net_cf > 0:
        insights.append(f"✅ Positive cash flow of ${net_cf:,.2f} indicates healthy financial operations")
        if cash_flow.get('cash_flow_ratio', 1) > 1.5:
            insights.append(f"🚀 Excellent cash flow ratio of {cash_flow['cash_flow_ratio']:.2f} shows strong financial stability")
    else:
        insights.append(f"⚠️ Negative cash flow of ${net_cf:,.2f} requires immediate attention")
        insights.append("💡 Consider implementing stricter credit terms and faster collection processes")
    
    # Income vs expenses analysis
    if total_income > 0 and total_expenses > 0:
        expense_ratio = total_expenses / total_income
        if expense_ratio > 0.9:
            insights.append(f"🔴 High expense ratio of {expense_ratio:.1%} - costs are consuming most of your income")
        elif expense_ratio < 0.7:
            insights.append(f"💚 Healthy expense ratio of {expense_ratio:.1%} shows good cost management")
    
    # Monthly average insights
    monthly_avg = cash_flow.get('monthly_average', 0)
    if monthly_avg != 0:
        if monthly_avg > 0:
            insights.append(f"📈 Average monthly cash flow of ${monthly_avg:,.2f} shows consistent performance")
        else:
            insights.append(f"📉 Average monthly cash flow of ${monthly_avg:,.2f} indicates structural issues")
    
    return insights

def _analyze_profitability(profitability):
    """Detailed profitability analysis with benchmarking."""
    if not profitability or 'gross_profit_margin' not in profitability:
        return ["Unable to analyze profitability - insufficient data"]
    
    insights = []
    margin = profitability['gross_profit_margin']
    gross_profit = profitability.get('gross_profit', 0)
    revenue = profitability.get('revenue', 0)
    
    # Margin analysis
    if margin > 0.4:
        insights.append(f"🌟 Exceptional profit margin of {margin:.1%} - you're operating very efficiently")
    elif margin > 0.2:
        insights.append(f"✅ Strong profit margin of {margin:.1%} - good pricing and cost control")
    elif margin > 0.1:
        insights.append(f"⚡ Moderate profit margin of {margin:.1%} - room for improvement")
    elif margin > 0:
        insights.append(f"⚠️ Low profit margin of {margin:.1%} - urgent optimization needed")
    else:
        insights.append(f"🔴 Operating at a loss with {margin:.1%} margin - immediate action required")
    
    # Revenue insights
    if revenue > 0:
        insights.append(f"💰 Total revenue of ${revenue:,.2f} with gross profit of ${gross_profit:,.2f}")
    
    # Break-even analysis
    if 'break_even_analysis' in profitability and 'break_even_transactions' in profitability['break_even_analysis']:
        be_analysis = profitability['break_even_analysis']
        current_transactions = be_analysis.get('current_transactions', 0)
        break_even_transactions = be_analysis.get('break_even_transactions', 0)
        
        if current_transactions > break_even_transactions:
            margin_of_safety = current_transactions - break_even_transactions
            insights.append(f"🛡️ Operating {margin_of_safety:.0f} transactions above break-even point")
        else:
            shortfall = break_even_transactions - current_transactions
            insights.append(f"⚠️ Need {shortfall:.0f} more transactions to reach break-even")
    
    return insights

def _analyze_trends(cash_flow_trend):
    """Advanced trend analysis with forecasting insights."""
    if not cash_flow_trend or 'trend_slope' not in cash_flow_trend:
        return ["Unable to analyze trends - insufficient historical data"]
    
    insights = []
    slope = cash_flow_trend['trend_slope']
    r_squared = cash_flow_trend.get('r_squared', 0)
    trajectory = cash_flow_trend.get('current_trajectory', 'unknown')
    
    # Trend direction analysis
    if slope > 0:
        insights.append(f"📈 Cash flow is trending upward with growth of ${slope:,.2f} per period")
        if r_squared > 0.7:
            insights.append(f"🎯 Strong trend reliability ({r_squared:.1%} confidence) suggests sustainable growth")
    else:
        insights.append(f"📉 Cash flow is declining by ${abs(slope):,.2f} per period")
        insights.append("🚨 Investigate underlying causes and implement corrective measures")
    
    # Volatility analysis
    volatility = cash_flow_trend.get('volatility', 0)
    if volatility > 0:
        if volatility < 1000:
            insights.append("🔄 Low volatility indicates stable and predictable cash flows")
        elif volatility > 5000:
            insights.append("⚡ High volatility suggests unpredictable cash flows - consider stabilization strategies")
    
    # Forecast insights
    forecast = cash_flow_trend.get('forecast', [])
    if forecast:
        avg_forecast = sum(forecast) / len(forecast)
        if avg_forecast > 0:
            insights.append(f"🔮 6-month forecast shows average monthly cash flow of ${avg_forecast:,.2f}")
        else:
            insights.append("⚠️ Forecast indicates potential cash flow challenges ahead")
    
    return insights

def _analyze_health_score(health_score):
    """Comprehensive financial health score analysis."""
    if not health_score or 'score' not in health_score:
        return ["Unable to calculate financial health score"]
    
    insights = []
    score = health_score['score']
    grade = health_score.get('grade', 'N/A')
    assessment = health_score.get('assessment', '')
    
    # Score interpretation
    if score >= 90:
        insights.append(f"🏆 Excellent financial health score of {score}/100 (Grade: {grade})")
        insights.append("🌟 Your business demonstrates exceptional financial management")
    elif score >= 70:
        insights.append(f"✅ Good financial health score of {score}/100 (Grade: {grade})")
        insights.append("💪 Strong financial foundation with minor areas for improvement")
    elif score >= 50:
        insights.append(f"⚡ Moderate financial health score of {score}/100 (Grade: {grade})")
        insights.append("🔧 Several opportunities to strengthen your financial position")
    else:
        insights.append(f"🔴 Poor financial health score of {score}/100 (Grade: {grade})")
        insights.append("🚨 Immediate action needed to improve financial stability")
    
    insights.append(f"📋 Assessment: {assessment}")
    
    return insights

def _assess_risks(cash_flow, profitability, cash_flow_trend):
    """AI-powered risk assessment with mitigation strategies."""
    risks = []
    
    # Liquidity risk
    if cash_flow.get('net_cash_flow', 0) < 0:
        risk_level = 'high' if cash_flow['net_cash_flow'] < -5000 else 'medium'
        risks.append({
            'type': 'liquidity',
            'level': risk_level,
            'description': 'Negative cash flow indicates immediate liquidity concerns',
            'mitigation': 'Accelerate receivables, delay payables, secure credit line'
        })
    
    # Profitability risk
    if profitability.get('gross_profit_margin', 0) < 0.05:
        risks.append({
            'type': 'profitability',
            'level': 'high',
            'description': 'Low profit margins threaten long-term sustainability',
            'mitigation': 'Review pricing strategy, optimize operations, reduce costs'
        })
    
    # Trend risk
    if cash_flow_trend.get('trend_slope', 0) < 0:
        risks.append({
            'type': 'trend',
            'level': 'medium',
            'description': 'Declining cash flow trend indicates potential future problems',
            'mitigation': 'Identify root causes, develop growth strategy, monitor closely'
        })
    
    # Volatility risk
    if cash_flow_trend.get('volatility', 0) > 5000:
        risks.append({
            'type': 'volatility',
            'level': 'medium',
            'description': 'High cash flow volatility makes planning difficult',
            'mitigation': 'Diversify revenue streams, implement better forecasting'
        })
    
    return risks

def _identify_opportunities(cash_flow, profitability, cash_flow_trend):
    """AI-powered opportunity identification."""
    opportunities = []
    
    # Investment opportunities
    if cash_flow.get('net_cash_flow', 0) > 10000:
        opportunities.append({
            'type': 'investment',
            'description': f"Strong cash position of ${cash_flow['net_cash_flow']:,.2f} enables growth investments",
            'potential': 'Invest in marketing, equipment, or expansion',
            'timeline': '1-3 months'
        })
    
    # Margin improvement
    if 0.1 < profitability.get('gross_profit_margin', 0) < 0.3:
        opportunities.append({
            'type': 'margin_improvement',
            'description': 'Moderate margins suggest room for optimization',
            'potential': 'Implement value-based pricing, reduce costs',
            'timeline': '2-6 months'
        })
    
    # Growth opportunities
    if cash_flow_trend.get('trend_slope', 0) > 0 and profitability.get('gross_profit_margin', 0) > 0.2:
        opportunities.append({
            'type': 'expansion',
            'description': 'Strong trends and margins indicate readiness for growth',
            'potential': 'Scale operations, enter new markets, hire staff',
            'timeline': '3-12 months'
        })
    
    # Efficiency opportunities
    expense_ratio = cash_flow.get('expense_ratio', 0)
    if expense_ratio > 0.8:
        opportunities.append({
            'type': 'efficiency',
            'description': 'High expense ratio suggests automation/optimization potential',
            'potential': 'Automate processes, renegotiate contracts, outsource',
            'timeline': '1-6 months'
        })
    
    return opportunities

def _calculate_overall_risk(alerts):
    """Calculate overall risk level based on alerts."""
    critical_count = len(alerts['critical_alerts'])
    warning_count = len(alerts['warning_alerts'])
    
    if critical_count > 2:
        return 'very_high'
    elif critical_count > 0:
        return 'high'
    elif warning_count > 3:
        return 'medium'
    elif warning_count > 0:
        return 'low'
    else:
        return 'minimal'

# Legacy function for backward compatibility
def generate_insights_legacy(cash_flow, profitability, cash_flow_trend):
    """
    Legacy function for backward compatibility.
    """
    suggestions = []

    # Cash Flow Insights
    if isinstance(cash_flow, dict):
        net_cf = cash_flow.get('net_cash_flow', cash_flow)
    else:
        net_cf = cash_flow
        
    if net_cf < 0:
        suggestions.append(f"Alert: Your cash flow is negative (${net_cf:,.2f}). You spent more than you earned. Review your expenses immediately.")
    else:
        suggestions.append(f"Good job: Your cash flow is positive (${net_cf:,.2f}), indicating a healthy cash position for the period.")

    # Profitability Insights
    if isinstance(profitability, dict):
        margin = profitability.get('gross_profit_margin', profitability)
    else:
        margin = profitability
        
    if margin < 0.1:
        suggestions.append(f"Action needed: Your net profit margin is low ({margin:.2%}). Explore ways to increase prices or reduce direct costs.")
    elif margin > 0.3:
        suggestions.append(f"Excellent: Your profit margin is strong ({margin:.2%}). This is a great sign of business efficiency.")
    else:
        suggestions.append(f"Solid performance: Your profit margin is healthy ({margin:.2%}). Keep monitoring your costs to maintain it.")

    # Cash Flow Trend Insights
    if isinstance(cash_flow_trend, dict):
        slope = cash_flow_trend.get('trend_slope', cash_flow_trend)
    else:
        slope = cash_flow_trend
        
    if slope < 0:
        suggestions.append(f"Warning: Your cash flow is trending downwards. Investigate the root cause, whether it's declining sales or rising costs.")
    elif slope > 0:
        suggestions.append("Positive trend: Your cash flow is growing over time. This is a great indicator of sustainable growth.")
    else:
        suggestions.append("Stable trend: Your cash flow appears to be stable. Look for opportunities to start an upward trend.")

    return suggestions
