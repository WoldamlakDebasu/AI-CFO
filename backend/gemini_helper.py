"""
Gemini AI Helper for intelligent financial data analysis.
Uses Google's Gemini AI to understand and process financial data with any structure.
"""

import google.generativeai as genai
import os
import json
import pandas as pd
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure Gemini API from environment variable
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

if GEMINI_API_KEY and GEMINI_API_KEY != "your_gemini_api_key_here":
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        MODEL = genai.GenerativeModel('gemini-pro')
        print("✅ Gemini API configured successfully!")
    except Exception as e:
        MODEL = None
        print(f"⚠️  Warning: Gemini API configuration failed: {e}")
        print("   AI features will use fallback pattern matching.")
else:
    MODEL = None
    print("⚠️  Warning: Gemini API key not found in .env file.")
    print("   AI features will use fallback pattern matching.")
    print("   To enable AI: Add GEMINI_API_KEY to your .env file")


class GeminiFinancialAnalyzer:
    """
    Uses Gemini AI to intelligently analyze financial data regardless of column structure.
    """
    
    @staticmethod
    def detect_column_mapping(df_sample, columns):
        """
        Use Gemini AI to detect which columns contain financial data.
        Returns a mapping of standard names to actual column names.
        """
        if MODEL is None:
            return GeminiFinancialAnalyzer._fallback_column_detection(columns)
        
        try:
            # Create a sample of the data
            sample_data = df_sample.head(5).to_string()
            
            prompt = f"""
            Analyze this financial data sample and identify the columns:
            
            Columns: {', '.join(columns)}
            
            Sample data:
            {sample_data}
            
            Please identify which columns contain:
            1. Date/Time information
            2. Income/Revenue (positive amounts)
            3. Expenses/Costs (amounts spent)
            4. Transaction amounts (if income/expense not separated)
            5. Category/Description/Type
            6. Any other relevant financial information
            
            Return your answer as a JSON object with this structure:
            {{
                "date_column": "actual_column_name or null",
                "income_column": "actual_column_name or null",
                "expense_column": "actual_column_name or null",
                "amount_column": "actual_column_name or null",
                "category_column": "actual_column_name or null",
                "description_column": "actual_column_name or null",
                "confidence": "high/medium/low",
                "suggestions": "any suggestions for better data structure"
            }}
            
            Return ONLY the JSON, no other text.
            """
            
            response = MODEL.generate_content(prompt)
            result = json.loads(response.text.strip())
            return result
            
        except Exception as e:
            print(f"Gemini API error: {e}")
            return GeminiFinancialAnalyzer._fallback_column_detection(columns)
    
    @staticmethod
    def _fallback_column_detection(columns):
        """
        Fallback column detection using pattern matching when AI is unavailable.
        """
        columns_lower = [col.lower() for col in columns]
        
        mapping = {
            "date_column": None,
            "income_column": None,
            "expense_column": None,
            "amount_column": None,
            "category_column": None,
            "description_column": None,
            "confidence": "medium"
        }
        
        # Date detection
        date_keywords = ['date', 'time', 'period', 'month', 'day', 'year', 'timestamp']
        for i, col in enumerate(columns_lower):
            if any(keyword in col for keyword in date_keywords):
                mapping['date_column'] = columns[i]
                break
        
        # Income detection
        income_keywords = ['income', 'revenue', 'sales', 'earning', 'receivable', 'credit']
        for i, col in enumerate(columns_lower):
            if any(keyword in col for keyword in income_keywords):
                mapping['income_column'] = columns[i]
                break
        
        # Expense detection
        expense_keywords = ['expense', 'cost', 'spending', 'payment', 'payable', 'debit']
        for i, col in enumerate(columns_lower):
            if any(keyword in col for keyword in expense_keywords):
                mapping['expense_column'] = columns[i]
                break
        
        # Amount detection (generic)
        amount_keywords = ['amount', 'value', 'total', 'sum', 'balance']
        for i, col in enumerate(columns_lower):
            if any(keyword in col for keyword in amount_keywords):
                mapping['amount_column'] = columns[i]
                break
        
        # Category detection
        category_keywords = ['category', 'type', 'class', 'group', 'account']
        for i, col in enumerate(columns_lower):
            if any(keyword in col for keyword in category_keywords):
                mapping['category_column'] = columns[i]
                break
        
        # Description detection
        desc_keywords = ['description', 'detail', 'note', 'memo', 'particular']
        for i, col in enumerate(columns_lower):
            if any(keyword in col for keyword in desc_keywords):
                mapping['description_column'] = columns[i]
                break
        
        return mapping
    
    @staticmethod
    def analyze_financial_data(df, column_mapping):
        """
        Use Gemini AI to provide insights on the financial data.
        """
        if MODEL is None:
            return {"analysis": "AI analysis unavailable - using basic analysis"}
        
        try:
            # Create summary statistics
            summary = {
                'row_count': len(df),
                'columns': list(df.columns),
                'date_range': None,
                'total_income': 0,
                'total_expenses': 0
            }
            
            # Get date range
            if column_mapping.get('date_column') and column_mapping['date_column'] in df.columns:
                date_col = df[column_mapping['date_column']]
                summary['date_range'] = f"{date_col.min()} to {date_col.max()}"
            
            # Calculate totals
            if column_mapping.get('income_column') and column_mapping['income_column'] in df.columns:
                summary['total_income'] = float(df[column_mapping['income_column']].sum())
            
            if column_mapping.get('expense_column') and column_mapping['expense_column'] in df.columns:
                summary['total_expenses'] = float(df[column_mapping['expense_column']].sum())
            
            # Get sample transactions
            sample_transactions = df.head(10).to_dict('records')
            
            prompt = f"""
            Analyze this financial data and provide insights:
            
            Summary:
            - Total rows: {summary['row_count']}
            - Date range: {summary['date_range']}
            - Total income: ${summary['total_income']:,.2f}
            - Total expenses: ${summary['total_expenses']:,.2f}
            
            Sample transactions:
            {json.dumps(sample_transactions, default=str, indent=2)[:1000]}
            
            Please provide:
            1. Key insights about the financial health
            2. Patterns or trends you notice
            3. Recommendations for improvement
            4. Any red flags or concerns
            
            Return your analysis as a JSON object with this structure:
            {{
                "health_status": "excellent/good/fair/poor",
                "key_insights": ["insight1", "insight2", ...],
                "trends": ["trend1", "trend2", ...],
                "recommendations": ["rec1", "rec2", ...],
                "red_flags": ["flag1", "flag2", ...],
                "summary": "brief overall summary"
            }}
            
            Return ONLY the JSON, no other text.
            """
            
            response = MODEL.generate_content(prompt)
            analysis = json.loads(response.text.strip())
            return analysis
            
        except Exception as e:
            print(f"Gemini analysis error: {e}")
            return {"analysis": f"AI analysis error: {str(e)}"}
    
    @staticmethod
    def generate_custom_insights(cash_flow, profitability, trends):
        """
        Generate custom insights using Gemini AI based on calculated metrics.
        """
        if MODEL is None:
            return ["AI insights unavailable"]
        
        try:
            prompt = f"""
            As a financial advisor, analyze these business metrics and provide actionable insights:
            
            Cash Flow:
            - Net cash flow: ${cash_flow.get('net_cash_flow', 0):,.2f}
            - Total income: ${cash_flow.get('total_income', 0):,.2f}
            - Total expenses: ${cash_flow.get('total_expenses', 0):,.2f}
            - Cash flow ratio: {cash_flow.get('cash_flow_ratio', 0):.2f}
            
            Profitability:
            - Gross profit: ${profitability.get('gross_profit', 0):,.2f}
            - Profit margin: {profitability.get('gross_profit_margin', 0):.1%}
            
            Trends:
            - Trend direction: {trends.get('current_trajectory', 'unknown')}
            - Trend slope: {trends.get('trend_slope', 0):.2f}
            
            Provide:
            1. 3-5 specific, actionable insights
            2. Each insight should be clear and practical
            3. Focus on what the business owner should do
            
            Return as a JSON array of strings: ["insight1", "insight2", ...]
            Return ONLY the JSON array, no other text.
            """
            
            response = MODEL.generate_content(prompt)
            insights = json.loads(response.text.strip())
            return insights if isinstance(insights, list) else [str(insights)]
            
        except Exception as e:
            print(f"Gemini insights error: {e}")
            return [f"Unable to generate AI insights: {str(e)}"]


def test_gemini_connection():
    """Test if Gemini API is properly configured."""
    if MODEL is None:
        return False, "API key not configured"
    
    try:
        response = MODEL.generate_content("Say 'Connected' if you can read this.")
        return True, response.text
    except Exception as e:
        return False, str(e)
