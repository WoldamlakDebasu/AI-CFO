# AI-CFO Sample Financial Data Files

This directory contains sample financial data files that you can use to test the AI-CFO application.

## Available Sample Files

### 1. **sample_financial_transactions.csv**
- **Best for:** Comprehensive financial analysis with detailed transactions
- **Contains:** 50+ transactions spanning 9 months (Jan-Sep 2024)
- **Features:**
  - Mix of income and expenses
  - Multiple expense categories (Rent, Salaries, Marketing, Utilities, etc.)
  - Revenue from different sources (Product Sales, Consulting, Services)
  - Shows business growth trend over time
- **Expected Analysis:**
  - Cash flow trend: Positive and growing
  - Health score: Good (60-80%)
  - Profitability: Increasing margins
  - Predictions: Continued growth trajectory

### 2. **sample_monthly_summary.csv**
- **Best for:** High-level monthly performance analysis
- **Contains:** 9 months of aggregated data (Jan-Sep 2024)
- **Features:**
  - Monthly revenue, costs, profit summaries
  - Clear cash flow trends
  - Operating expense tracking
  - Steady growth pattern
- **Expected Analysis:**
  - Strong profitability trend
  - Decreasing cost-to-revenue ratio
  - Health score: Excellent (75-90%)
  - Predictions: Strong future performance

### 3. **sample_small_business.csv**
- **Best for:** Service-based business analysis
- **Contains:** 75+ transactions for a tech consulting/development business
- **Features:**
  - Project-based income tracking
  - Recurring expenses (rent, subscriptions, cloud services)
  - Variable costs (freelancers, marketing)
  - Diverse revenue streams
- **Expected Analysis:**
  - Positive cash flow with variability
  - Good profit margins on services
  - Health score: Good to Excellent (70-85%)
  - Seasonal patterns identified

## How to Use

1. **Start the Application:**
   - Backend should be running on `http://localhost:5000`
   - Frontend should be running on `http://localhost:5173`

2. **Upload a Sample File:**
   - Navigate to the file upload section in the UI
   - Select one of these sample CSV files
   - (Optional) Select industry type and business size for better benchmarking

3. **Review the Analysis:**
   The AI-CFO will provide:
   - **Cash Flow Analysis**: Income, expenses, and net cash flow
   - **Profitability Metrics**: Profit margins, revenue trends
   - **Financial Health Score**: Overall business health rating
   - **Trend Analysis**: Growth patterns and predictions
   - **Anomaly Detection**: Unusual transactions or patterns
   - **AI Insights**: Personalized recommendations
   - **Industry Benchmarks**: Comparison with industry standards
   - **Financial Alerts**: Critical issues requiring attention
   - **Future Predictions**: 3-month revenue and cash flow forecasts

## Data Format Requirements

Your CSV files should include at least one of these column combinations:

**Option 1:** Separate Income/Expense columns
- `Date`, `Income`, `Expenses`

**Option 2:** Amount with Category
- `Date`, `Amount`, `Category` (where category contains keywords like "income", "expense", "revenue", "cost")

**Optional columns** for enhanced analysis:
- `Description`, `Type`, `Revenue`, `Costs`, `Profit`, `Cash_Flow`

## Tips for Best Results

1. **More data = Better predictions**: Upload at least 3-6 months of data
2. **Consistent formatting**: Keep date formats consistent
3. **Clear categorization**: Use descriptive categories for transactions
4. **Include context**: The more detailed your descriptions, the better the AI insights
5. **Regular updates**: Upload updated data monthly for trend tracking

## Creating Your Own Data Files

To create your own financial data file:

1. Export data from your accounting software (QuickBooks, Xero, etc.)
2. Format as CSV with required columns
3. Ensure dates are in YYYY-MM-DD format
4. Remove any currency symbols (the system handles these automatically)
5. Upload and let AI-CFO do the rest!

---

**Need help?** Check the main README.md for more information about the AI-CFO application.
