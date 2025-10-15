from models import FinancialData, BenchmarkAnalysis
from utils import generate_insights, generate_recommendations, create_financial_alerts
import json
import pandas as pd
from datetime import datetime

class FinancialAnalysisService:
    """
    Advanced financial analysis service with AI-powered insights.
    """
    
    @staticmethod
    def process_financial_data(file, user_industry='default', business_size='small'):
        """
        Comprehensive financial data processing with AI insights.
        """
        try:
            financial_data = FinancialData(file)
            
            # Core financial metrics
            cash_flow = financial_data.get_cash_flow()
            profitability = financial_data.get_profitability()
            cash_flow_trend = financial_data.get_cash_flow_trend()
            health_score = financial_data.get_financial_health_score()
            anomalies = financial_data.detect_anomalies()
            
            # Handle cases where profitability can't be calculated
            if 'error' in profitability:
                profitability_metrics = {
                    'gross_profit': 'N/A',
                    'gross_profit_margin': 'N/A',
                    'revenue': 'N/A',
                    'costs': 'N/A',
                    'profit_per_transaction': 'N/A',
                    'break_even_analysis': {'error': 'Not enough data'},
                    'profitability_trend': 'N/A'
                }
            else:
                profitability_metrics = profitability

            # Industry benchmarking
            benchmark_comparison = BenchmarkAnalysis.compare_to_industry(
                financial_data, industry=user_industry
            )
            
            # AI-generated insights and recommendations
            ai_insights = generate_insights(cash_flow, profitability_metrics, cash_flow_trend, health_score)
            recommendations = generate_recommendations(
                cash_flow, profitability_metrics, cash_flow_trend, benchmark_comparison, business_size
            )
            alerts = create_financial_alerts(cash_flow, profitability_metrics, anomalies, health_score)
            
            # Prepare comprehensive analysis result
            analysis_result = {
                'timestamp': datetime.now().isoformat(),
                'file_processed': file.filename,
                'data_quality': {
                    'rows_processed': len(financial_data.df),
                    'columns_found': list(financial_data.df.columns),
                    'date_range': _get_date_range(financial_data.df),
                    'completeness_score': _calculate_data_completeness(financial_data.df)
                },
                'financial_metrics': {
                    'cash_flow': cash_flow,
                    'profitability': profitability_metrics,
                    'trend_analysis': cash_flow_trend,
                    'health_score': health_score,
                    'anomalies': anomalies
                },
                'benchmark_analysis': benchmark_comparison,
                'ai_insights': ai_insights,
                'recommendations': recommendations,
                'alerts': alerts,
                'forecast': _generate_forecast(cash_flow_trend),
                'action_items': _generate_action_items(recommendations, alerts),
                'executive_summary': _generate_executive_summary(
                    health_score, cash_flow, profitability_metrics, recommendations
                )
            }
            
            return analysis_result
            
        except Exception as e:
            import traceback
            error_details = traceback.format_exc()
            print(f"Analysis error: {error_details}")
            
            error_response = {
                'error': True,
                'message': f"Analysis failed: {str(e)}",
                'error_type': type(e).__name__,
                'suggestions': [
                    "✓ Your file will be analyzed automatically - we support ANY column structure!",
                    "✓ Our AI will detect columns containing financial data",
                    "✓ Supported: dates, amounts, income, expenses, categories",
                    "✓ If you see this error, please check the file format (CSV or Excel)",
                    f"✓ Technical details: {str(e)}"
                ],
                'supported_formats': {
                    'file_types': ['CSV (.csv)', 'Excel (.xlsx, .xls)'],
                    'column_flexibility': 'Any column names will work - AI will detect them',
                    'example_columns': ['date/amount/category', 'Date/Income/Expenses', 'Time/Revenue/Cost']
                },
                'timestamp': datetime.now().isoformat()
            }
            return error_response

    @staticmethod
    def get_data_template():
        """
        Provides data format templates for different business types.
        """
        templates = {
            'basic_template': {
                'columns': ['date', 'description', 'amount', 'category'],
                'example_data': [
                    ['2024-01-01', 'Client Payment', '5000', 'income'],
                    ['2024-01-02', 'Office Rent', '-1200', 'expense'],
                    ['2024-01-03', 'Software License', '-299', 'expense']
                ]
            },
            'detailed_template': {
                'columns': ['date', 'description', 'income', 'expenses', 'category', 'client'],
                'example_data': [
                    ['2024-01-01', 'Consulting Services', '5000', '0', 'revenue', 'Client A'],
                    ['2024-01-02', 'Office Rent', '0', '1200', 'overhead', 'Landlord'],
                    ['2024-01-03', 'Marketing Campaign', '0', '800', 'marketing', 'Ad Agency']
                ]
            },
            'retail_template': {
                'columns': ['date', 'product', 'revenue', 'cost_of_goods', 'category'],
                'example_data': [
                    ['2024-01-01', 'Product A', '150', '75', 'sales'],
                    ['2024-01-02', 'Product B', '200', '120', 'sales'],
                    ['2024-01-03', 'Inventory Purchase', '0', '1000', 'inventory']
                ]
            }
        }
        return templates

    @staticmethod
    def export_analysis(analysis_result, format_type='json'):
        """
        Export analysis results in various formats.
        """
        if format_type == 'json':
            return json.dumps(analysis_result, indent=2, default=str)
        elif format_type == 'summary':
            return _create_text_summary(analysis_result)
        elif format_type == 'csv':
            return _create_csv_export(analysis_result)
        else:
            return analysis_result

def _get_date_range(df):
    """Get the date range of the financial data."""
    if 'date' in df.columns:
        return {
            'start_date': df['date'].min().isoformat() if pd.notna(df['date'].min()) else None,
            'end_date': df['date'].max().isoformat() if pd.notna(df['date'].max()) else None,
            'period_months': (df['date'].max() - df['date'].min()).days / 30 if pd.notna(df['date'].max()) and pd.notna(df['date'].min()) else 0
        }
    return {'start_date': None, 'end_date': None, 'period_months': 0}

def _calculate_data_completeness(df):
    """Calculate data completeness score."""
    total_cells = df.size
    non_null_cells = df.count().sum()
    return (non_null_cells / total_cells * 100) if total_cells > 0 else 0

def _generate_forecast(trend_data):
    """Generate financial forecast based on trend analysis."""
    if not trend_data or 'forecast' not in trend_data:
        return {'error': 'Insufficient data for forecasting'}
    
    forecast_data = {
        'next_6_months': trend_data.get('forecast', []),
        'confidence_level': 'medium' if trend_data.get('r_squared', 0) > 0.5 else 'low',
        'assumptions': [
            'Based on historical trend patterns',
            'Assumes no major business changes',
            'External factors not considered'
        ],
        'scenario_analysis': {
            'optimistic': [x * 1.2 for x in trend_data.get('forecast', [])],
            'pessimistic': [x * 0.8 for x in trend_data.get('forecast', [])],
            'realistic': trend_data.get('forecast', [])
        }
    }
    
    return forecast_data

def _generate_action_items(recommendations, alerts):
    """Generate prioritized action items."""
    action_items = []
    
    # High priority from alerts
    for alert in alerts.get('critical_alerts', []):
        action_items.append({
            'priority': 'high',
            'category': 'alert',
            'action': alert,
            'timeline': 'immediate'
        })
    
    # Medium priority from recommendations
    for rec in recommendations.get('immediate_actions', []):
        action_items.append({
            'priority': 'medium',
            'category': 'improvement',
            'action': rec,
            'timeline': '1-2 weeks'
        })
    
    # Low priority strategic items
    for rec in recommendations.get('strategic_recommendations', []):
        action_items.append({
            'priority': 'low',
            'category': 'strategic',
            'action': rec,
            'timeline': '1-3 months'
        })
    
    return action_items

def _generate_executive_summary(health_score, cash_flow, profitability, recommendations):
    """Generate executive summary of financial analysis."""
    summary = {
        'overall_health': health_score.get('grade', 'N/A'),
        'key_findings': [],
        'critical_issues': [],
        'opportunities': [],
        'next_steps': []
    }
    
    # Key findings
    if cash_flow.get('net_cash_flow', 0) > 0:
        summary['key_findings'].append(f"Positive cash flow of ${cash_flow['net_cash_flow']:,.2f}")
    else:
        summary['critical_issues'].append(f"Negative cash flow of ${cash_flow['net_cash_flow']:,.2f}")
    
    gpm = profitability.get('gross_profit_margin')
    if isinstance(gpm, (int, float)) and gpm > 0.15:
        summary['key_findings'].append(f"Strong profit margin of {gpm:.1%}")
    elif isinstance(gpm, (int, float)) and gpm > 0:
        summary['opportunities'].append("Opportunity to improve profit margins")
    else:
        summary['critical_issues'].append("Operating at a loss or unable to calculate profitability")
    
    # Next steps from recommendations
    immediate_actions = recommendations.get('immediate_actions', [])
    if immediate_actions:
        summary['next_steps'] = immediate_actions[:3]  # Top 3 actions
    
    return summary

def _create_text_summary(analysis_result):
    """Create a text summary of the analysis."""
    summary_text = f"""
FINANCIAL ANALYSIS SUMMARY
Generated: {analysis_result['timestamp']}
File: {analysis_result['file_processed']}

OVERALL HEALTH SCORE: {analysis_result['financial_metrics']['health_score']['score']}/100 ({analysis_result['financial_metrics']['health_score']['grade']})

KEY METRICS:
- Cash Flow: ${analysis_result['financial_metrics']['cash_flow'].get('net_cash_flow', 0):,.2f}
- Profit Margin: {analysis_result['financial_metrics']['profitability'].get('gross_profit_margin', 0):.1%}
- Financial Health: {analysis_result['financial_metrics']['health_score']['assessment']}

TOP RECOMMENDATIONS:
"""
    
    for i, rec in enumerate(analysis_result['recommendations'].get('immediate_actions', [])[:3], 1):
        summary_text += f"{i}. {rec}\n"
    
    return summary_text

def _create_csv_export(analysis_result):
    """Create CSV export of key metrics."""
    import io
    import csv
    
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Headers
    writer.writerow(['Metric', 'Value', 'Status'])
    
    # Key metrics
    cash_flow = analysis_result['financial_metrics']['cash_flow']
    profitability = analysis_result['financial_metrics']['profitability']
    health_score = analysis_result['financial_metrics']['health_score']
    
    writer.writerow(['Cash Flow', f"${cash_flow.get('net_cash_flow', 0):,.2f}", 'Positive' if cash_flow.get('net_cash_flow', 0) > 0 else 'Negative'])
    writer.writerow(['Profit Margin', f"{profitability.get('gross_profit_margin', 0):.1%}", 'Good' if profitability.get('gross_profit_margin', 0) > 0.1 else 'Needs Improvement'])
    writer.writerow(['Health Score', f"{health_score['score']}/100", health_score['grade']])
    
    return output.getvalue()

# Legacy function for backward compatibility
def process_financial_data(file):
    """Legacy function - redirects to new service."""
    return FinancialAnalysisService.process_financial_data(file)
