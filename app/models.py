import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import IsolationForest
import numpy as np
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

class FinancialData:
    """
    Advanced financial data processor with AI-powered insights.
    Supports multiple data formats and provides comprehensive financial analysis.
    """
    def __init__(self, file):
        # Support multiple file formats
        if file.filename.endswith('.xlsx') or file.filename.endswith('.xls'):
            self.df = pd.read_excel(file)
        else:
            self.df = pd.read_csv(file)
        
        # Advanced data cleaning and preprocessing
        self.df.columns = self.df.columns.str.strip().str.lower().str.replace(' ', '_')
        self._standardize_columns()
        self._ensure_income_expenses()
        self._clean_data()
        
    def _standardize_columns(self):
        """Standardize column names across different data formats"""
        column_mapping = {
            'revenue': ['sales', 'income', 'turnover', 'gross_sales'],
            'expenses': ['costs', 'expenditure', 'outgoings', 'spending'],
            'date': ['transaction_date', 'period', 'month', 'time'],
            'amount': ['value', 'sum', 'total'],
            'category': ['type', 'description', 'account', 'classification']
        }
        
        for standard_name, variations in column_mapping.items():
            for col in self.df.columns:
                if any(var in col for var in variations):
                    self.df.rename(columns={col: standard_name}, inplace=True)
                    break

    def _ensure_income_expenses(self):
        """Ensure income and expenses columns exist, creating them if necessary."""
        if 'revenue' in self.df.columns and 'income' not in self.df.columns:
            self.df['income'] = self.df['revenue']

        if 'amount' in self.df.columns and 'category' in self.df.columns:
            if 'income' not in self.df.columns:
                income_keywords = ['income', 'revenue', 'sales', 'receivable', 'deposit']
                income_mask = self.df['category'].str.lower().str.contains('|'.join(income_keywords), na=False)
                self.df.loc[income_mask, 'income'] = self.df.loc[income_mask, 'amount']

            if 'expenses' not in self.df.columns:
                expense_keywords = ['expense', 'cost', 'payment', 'bill', 'payable', 'purchase']
                expense_mask = self.df['category'].str.lower().str.contains('|'.join(expense_keywords), na=False)
                self.df.loc[expense_mask, 'expenses'] = self.df.loc[expense_mask, 'amount']
    
    def _clean_data(self):
        """Advanced data cleaning and validation"""
        # Convert date column
        if 'date' in self.df.columns:
            self.df['date'] = pd.to_datetime(self.df['date'], errors='coerce')
            # Remove rows with invalid dates
            self.df = self.df.dropna(subset=['date'])
        
        # Clean numerical columns
        numerical_cols = ['amount', 'revenue', 'expenses', 'income']
        for col in numerical_cols:
            if col in self.df.columns:
                # Remove currency symbols and convert to float
                self.df[col] = self.df[col].astype(str).str.replace(r'[$,£€¥]', '', regex=True)
                self.df[col] = pd.to_numeric(self.df[col], errors='coerce')
        
        # Remove rows with critical missing data
        self.df = self.df.dropna(subset=[col for col in numerical_cols if col in self.df.columns])

    def get_cash_flow(self):
        """
        Calculates comprehensive cash flow analysis with AI insights.
        """
        cash_flow_data = {}
        
        if 'income' in self.df.columns and 'expenses' in self.df.columns:
            total_income = self.df['income'].sum()
            total_expenses = self.df['expenses'].sum()
            net_cash_flow = total_income - total_expenses
        elif 'amount' in self.df.columns and 'category' in self.df.columns:
            income_keywords = ['income', 'revenue', 'sales', 'receivable', 'deposit']
            expense_keywords = ['expense', 'cost', 'payment', 'bill', 'payable', 'purchase']
            
            income_mask = self.df['category'].str.lower().str.contains('|'.join(income_keywords), na=False)
            expense_mask = self.df['category'].str.lower().str.contains('|'.join(expense_keywords), na=False)
            
            total_income = self.df[income_mask]['amount'].sum()
            total_expenses = self.df[expense_mask]['amount'].sum()
            net_cash_flow = total_income - total_expenses
        else:
            return {'error': 'Unable to identify income and expense columns'}
        
        # Calculate cash flow metrics
        cash_flow_data = {
            'net_cash_flow': float(net_cash_flow),
            'total_income': float(total_income),
            'total_expenses': float(total_expenses),
            'cash_flow_ratio': float(total_income / total_expenses) if total_expenses > 0 else float('inf'),
            'expense_ratio': float(total_expenses / total_income) if total_income > 0 else 0,
            'monthly_average': self._get_monthly_cash_flow_average(),
            'seasonal_analysis': self._get_seasonal_patterns()
        }
        
        return cash_flow_data

    def get_profitability(self):
        """
        Advanced profitability analysis with multiple metrics.
        """
        revenue = self._get_total_revenue()
        costs = self._get_total_costs()
        
        if revenue <= 0:
            return {'error': 'No revenue data found'}
        
        gross_profit = revenue - costs
        profitability_metrics = {
            'gross_profit': float(gross_profit),
            'gross_profit_margin': float(gross_profit / revenue),
            'revenue': float(revenue),
            'costs': float(costs),
            'profit_per_transaction': self._get_profit_per_transaction(),
            'break_even_analysis': self._calculate_break_even(),
            'profitability_trend': self._get_profitability_trend()
        }
        
        return profitability_metrics

    def get_cash_flow_trend(self):
        """
        Advanced cash flow trend analysis with forecasting.
        """
        if 'date' not in self.df.columns:
            return {'error': 'Date column required for trend analysis'}
        
        # Create monthly aggregations
        self.df = self.df.sort_values('date')
        monthly_data = self._create_monthly_aggregations()
        
        if len(monthly_data) < 2:
            return {'error': 'Insufficient data for trend analysis'}
        
        # Perform trend analysis
        X = np.arange(len(monthly_data)).reshape(-1, 1)
        y = monthly_data['net_cash_flow'].values
        
        model = LinearRegression()
        model.fit(X, y)
        
        # Generate forecast
        future_periods = 6
        future_X = np.arange(len(monthly_data), len(monthly_data) + future_periods).reshape(-1, 1)
        forecast = model.predict(future_X)
        
        trend_data = {
            'trend_slope': float(model.coef_[0]),
            'r_squared': float(model.score(X, y)),
            'current_trajectory': 'improving' if model.coef_[0] > 0 else 'declining',
            'monthly_data': monthly_data.to_dict('records'),
            'forecast': forecast.tolist(),
            'volatility': float(np.std(y)),
            'trend_strength': self._calculate_trend_strength(y)
        }
        
        return trend_data

    def detect_anomalies(self):
        """
        AI-powered anomaly detection for unusual financial patterns.
        """
        if len(self.df) < 10:
            return {'error': 'Insufficient data for anomaly detection'}
        
        # Prepare features for anomaly detection
        features = []
        if 'amount' in self.df.columns:
            features.append('amount')
        
        if not features:
            return {'error': 'No suitable columns for anomaly detection'}
        
        # Use Isolation Forest for anomaly detection
        X = self.df[features].fillna(0)
        iso_forest = IsolationForest(contamination=0.1, random_state=42)
        anomalies = iso_forest.fit_predict(X)
        
        anomaly_indices = np.where(anomalies == -1)[0]
        anomaly_data = self.df.iloc[anomaly_indices].copy()
        
        return {
            'anomaly_count': len(anomaly_indices),
            'anomaly_percentage': float(len(anomaly_indices) / len(self.df) * 100),
            'anomalies': anomaly_data.to_dict('records') if len(anomaly_data) < 20 else anomaly_data.head(20).to_dict('records'),
            'total_anomaly_value': float(anomaly_data['amount'].sum()) if 'amount' in anomaly_data.columns else 0
        }

    def get_financial_health_score(self):
        """
        Calculate comprehensive financial health score (0-100).
        """
        score = 0
        max_score = 100
        
        # Cash flow health (30 points)
        cash_flow_data = self.get_cash_flow()
        if 'net_cash_flow' in cash_flow_data:
            if cash_flow_data['net_cash_flow'] > 0:
                score += 20
                if cash_flow_data['cash_flow_ratio'] > 1.2:
                    score += 10
        
        # Profitability health (30 points)
        prof_data = self.get_profitability()
        if 'gross_profit_margin' in prof_data:
            margin = prof_data['gross_profit_margin']
            if margin > 0.3:
                score += 30
            elif margin > 0.15:
                score += 20
            elif margin > 0.05:
                score += 10
        
        # Trend health (25 points)
        trend_data = self.get_cash_flow_trend()
        if 'trend_slope' in trend_data:
            if trend_data['trend_slope'] > 0:
                score += 15
                if trend_data['r_squared'] > 0.7:
                    score += 10
        
        # Consistency health (15 points)
        if 'volatility' in trend_data:
            if trend_data['volatility'] < np.mean([abs(cash_flow_data.get('total_income', 0)), abs(cash_flow_data.get('total_expenses', 0))]) * 0.1:
                score += 15
            elif trend_data['volatility'] < np.mean([abs(cash_flow_data.get('total_income', 0)), abs(cash_flow_data.get('total_expenses', 0))]) * 0.2:
                score += 10
        
        return {
            'score': min(score, max_score),
            'grade': self._score_to_grade(min(score, max_score)),
            'assessment': self._get_health_assessment(min(score, max_score))
        }

    def _get_total_revenue(self):
        """Helper method to calculate total revenue"""
        if 'revenue' in self.df.columns:
            return self.df['revenue'].sum()
        elif 'income' in self.df.columns:
            return self.df['income'].sum()
        elif 'amount' in self.df.columns and 'category' in self.df.columns:
            income_mask = self.df['category'].str.lower().str.contains('income|revenue|sales', na=False)
            return self.df[income_mask]['amount'].sum()
        return 0

    def _get_total_costs(self):
        """Helper method to calculate total costs"""
        if 'costs' in self.df.columns:
            return self.df['costs'].sum()
        elif 'expenses' in self.df.columns:
            return self.df['expenses'].sum()
        elif 'amount' in self.df.columns and 'category' in self.df.columns:
            expense_mask = self.df['category'].str.lower().str.contains('expense|cost|payment|bill', na=False)
            return self.df[expense_mask]['amount'].sum()
        return 0

    def _create_monthly_aggregations(self):
        """Create monthly financial aggregations"""
        agg_dict = {}
        
        if 'amount' in self.df.columns:
            agg_dict['amount'] = 'sum'
        if 'income' in self.df.columns:
            agg_dict['income'] = 'sum'
        if 'expenses' in self.df.columns:
            agg_dict['expenses'] = 'sum'
        
        if not agg_dict:
            # Return empty dataframe if no valid columns
            return pd.DataFrame({'net_cash_flow': []})
        
        monthly = self.df.set_index('date').resample('M').agg(agg_dict)
        
        # Ensure monthly is a DataFrame
        if isinstance(monthly, pd.Series):
            monthly = monthly.to_frame()
        
        # Calculate net cash flow
        if 'income' in monthly.columns and 'expenses' in monthly.columns:
            monthly['net_cash_flow'] = monthly['income'] - monthly['expenses']
        elif 'amount' in monthly.columns:
            # Estimate from amount
            monthly['net_cash_flow'] = monthly['amount']
        else:
            monthly['net_cash_flow'] = 0
        
        return monthly.reset_index()

    def _get_monthly_cash_flow_average(self):
        """Calculate monthly cash flow average"""
        if 'date' not in self.df.columns:
            return 0
        
        monthly_data = self._create_monthly_aggregations()
        return float(monthly_data['net_cash_flow'].mean()) if len(monthly_data) > 0 else 0

    def _get_seasonal_patterns(self):
        """Analyze seasonal patterns in cash flow"""
        if 'date' not in self.df.columns or len(self.df) < 12:
            return {}
        
        self.df['month'] = self.df['date'].dt.month
        monthly_avg = self.df.groupby('month')['amount'].mean() if 'amount' in self.df.columns else {}
        
        return monthly_avg.to_dict() if hasattr(monthly_avg, 'to_dict') else {}

    def _get_profit_per_transaction(self):
        """Calculate average profit per transaction"""
        total_transactions = len(self.df)
        if total_transactions == 0:
            return 0
        
        revenue = self._get_total_revenue()
        costs = self._get_total_costs()
        return float((revenue - costs) / total_transactions)

    def _calculate_break_even(self):
        """Calculate break-even analysis"""
        fixed_costs = self._estimate_fixed_costs()
        variable_cost_ratio = self._estimate_variable_cost_ratio()
        avg_revenue_per_transaction = self._get_total_revenue() / len(self.df) if len(self.df) > 0 else 0
        
        if avg_revenue_per_transaction > 0 and variable_cost_ratio < 1:
            contribution_margin = avg_revenue_per_transaction * (1 - variable_cost_ratio)
            break_even_transactions = fixed_costs / contribution_margin if contribution_margin > 0 else float('inf')
            return {
                'break_even_transactions': float(break_even_transactions),
                'break_even_revenue': float(break_even_transactions * avg_revenue_per_transaction),
                'current_transactions': len(self.df),
                'margin_of_safety': float(len(self.df) - break_even_transactions) if break_even_transactions != float('inf') else 0
            }
        
        return {'error': 'Insufficient data for break-even analysis'}

    def _estimate_fixed_costs(self):
        """Estimate fixed costs from expense patterns"""
        if 'expenses' in self.df.columns:
            return float(self.df['expenses'].quantile(0.1))  # Bottom 10% as proxy for fixed costs
        return 0

    def _estimate_variable_cost_ratio(self):
        """Estimate variable cost ratio"""
        total_revenue = self._get_total_revenue()
        total_costs = self._get_total_costs()
        return float(total_costs / total_revenue) if total_revenue > 0 else 0

    def _get_profitability_trend(self):
        """Calculate profitability trend over time"""
        if 'date' not in self.df.columns:
            return 0
        
        monthly_data = self._create_monthly_aggregations()
        if len(monthly_data) < 2:
            return 0
        
        monthly_data['profit_margin'] = (monthly_data['income'] - monthly_data['expenses']) / monthly_data['income']
        monthly_data['profit_margin'] = monthly_data['profit_margin'].fillna(0)
        
        X = np.arange(len(monthly_data)).reshape(-1, 1)
        y = monthly_data['profit_margin'].values
        
        model = LinearRegression()
        model.fit(X, y)
        
        return float(model.coef_[0])

    def _calculate_trend_strength(self, values):
        """Calculate strength of trend (0-1)"""
        if len(values) < 3:
            return 0
        
        # Calculate correlation with time
        time_series = np.arange(len(values))
        correlation = np.corrcoef(time_series, values)[0, 1]
        return abs(correlation)

    def _score_to_grade(self, score):
        """Convert numerical score to letter grade"""
        if score >= 90:
            return 'A+'
        elif score >= 80:
            return 'A'
        elif score >= 70:
            return 'B'
        elif score >= 60:
            return 'C'
        elif score >= 50:
            return 'D'
        else:
            return 'F'

    def _get_health_assessment(self, score):
        """Get textual assessment of financial health"""
        if score >= 80:
            return 'Excellent financial health with strong performance indicators'
        elif score >= 60:
            return 'Good financial health with some areas for improvement'
        elif score >= 40:
            return 'Moderate financial health requiring attention to key areas'
        else:
            return 'Poor financial health requiring immediate action'


class BenchmarkAnalysis:
    """
    Industry benchmark comparison and competitive analysis.
    """
    
    # Industry benchmarks by business type
    INDUSTRY_BENCHMARKS = {
        'retail': {'profit_margin': 0.05, 'cash_flow_ratio': 1.15, 'expense_ratio': 0.85},
        'services': {'profit_margin': 0.15, 'cash_flow_ratio': 1.25, 'expense_ratio': 0.75},
        'manufacturing': {'profit_margin': 0.08, 'cash_flow_ratio': 1.20, 'expense_ratio': 0.80},
        'technology': {'profit_margin': 0.25, 'cash_flow_ratio': 1.40, 'expense_ratio': 0.65},
        'consulting': {'profit_margin': 0.20, 'cash_flow_ratio': 1.30, 'expense_ratio': 0.70},
        'default': {'profit_margin': 0.10, 'cash_flow_ratio': 1.20, 'expense_ratio': 0.80}
    }
    
    @classmethod
    def compare_to_industry(cls, financial_data, industry='default'):
        """
        Compare business performance to industry benchmarks.
        """
        benchmarks = cls.INDUSTRY_BENCHMARKS.get(industry, cls.INDUSTRY_BENCHMARKS['default'])
        
        cash_flow = financial_data.get_cash_flow()
        profitability = financial_data.get_profitability()
        
        comparison = {}
        
        if 'gross_profit_margin' in profitability:
            margin_diff = profitability['gross_profit_margin'] - benchmarks['profit_margin']
            comparison['profit_margin'] = {
                'your_performance': profitability['gross_profit_margin'],
                'industry_benchmark': benchmarks['profit_margin'],
                'difference': margin_diff,
                'performance': 'above' if margin_diff > 0 else 'below',
                'percentile': cls._calculate_percentile(margin_diff, 'profit_margin')
            }
        
        if 'cash_flow_ratio' in cash_flow:
            ratio_diff = cash_flow['cash_flow_ratio'] - benchmarks['cash_flow_ratio']
            comparison['cash_flow_ratio'] = {
                'your_performance': cash_flow['cash_flow_ratio'],
                'industry_benchmark': benchmarks['cash_flow_ratio'],
                'difference': ratio_diff,
                'performance': 'above' if ratio_diff > 0 else 'below',
                'percentile': cls._calculate_percentile(ratio_diff, 'cash_flow_ratio')
            }
        
        if 'expense_ratio' in cash_flow:
            expense_diff = benchmarks['expense_ratio'] - cash_flow['expense_ratio']  # Lower is better
            comparison['expense_ratio'] = {
                'your_performance': cash_flow['expense_ratio'],
                'industry_benchmark': benchmarks['expense_ratio'],
                'difference': expense_diff,
                'performance': 'above' if expense_diff > 0 else 'below',
                'percentile': cls._calculate_percentile(expense_diff, 'expense_ratio')
            }
        
        return comparison
    
    @classmethod
    def _calculate_percentile(cls, difference, metric_type):
        """
        Estimate percentile based on difference from benchmark.
        """
        # Simplified percentile calculation
        if metric_type == 'profit_margin':
            if difference > 0.05:
                return 90
            elif difference > 0.02:
                return 75
            elif difference > -0.02:
                return 50
            else:
                return 25
        elif metric_type == 'cash_flow_ratio':
            if difference > 0.2:
                return 90
            elif difference > 0.1:
                return 75
            elif difference > -0.1:
                return 50
            else:
                return 25
        elif metric_type == 'expense_ratio':
            if difference > 0.1:
                return 90
            elif difference > 0.05:
                return 75
            elif difference > -0.05:
                return 50
            else:
                return 25
        
        return 50  # Default to median
