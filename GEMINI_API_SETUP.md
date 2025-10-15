# Gemini API Integration Guide

## Overview
Your AI-CFO application now uses Google's Gemini AI to intelligently analyze financial data with ANY column structure. The AI automatically detects and understands your data format!

## Features Added

### 1. **Intelligent Column Detection**
- The system now uses Gemini AI to automatically detect which columns contain:
  - Date/Time information
  - Income/Revenue
  - Expenses/Costs
  - Transaction amounts
  - Categories/Descriptions
- Works with ANY column names!

### 2. **Flexible Data Processing**
- No longer requires specific column names like 'income' or 'expenses'
- Handles various formats:
  - `Date, Amount, Category`
  - `Time, Revenue, Cost`
  - `Period, Income, Expenses`
  - And many more!

### 3. **AI-Powered Insights**
- Gemini AI generates custom insights based on your specific data
- Provides actionable recommendations
- Identifies patterns and trends

## API Key Setup

### Your Current API Key
The Gemini API key is already configured in the file:
```
backend/gemini_helper.py
```

**Current Key:** `AIzaSyBQvDVCfXpxpM3_yBIbWoqqXBdjQwRJMNM`

### To Update Your API Key

1. **Get a Free Gemini API Key:**
   - Visit: https://makersuite.google.com/app/apikey
   - Sign in with your Google account
   - Click "Create API Key"
   - Copy your new API key

2. **Update the Key in Code:**
   Open `backend/gemini_helper.py` and find this line:
   ```python
   GEMINI_API_KEY = "AIzaSyBQvDVCfXpxpM3_yBIbWoqqXBdjQwRJMNM"
   ```
   
   Replace it with your new key:
   ```python
   GEMINI_API_KEY = "your_new_api_key_here"
   ```

3. **Better Method - Use Environment Variable (Recommended):**
   ```python
   import os
   GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', 'your_fallback_key_here')
   ```
   
   Then set the environment variable:
   - Windows: `set GEMINI_API_KEY=your_key_here`
   - Linux/Mac: `export GEMINI_API_KEY=your_key_here`

## How It Works

### 1. File Upload
When a user uploads a CSV or Excel file:

```python
# The system reads the file
file = request.files['file']

# AI analyzes the structure
column_mapping = GeminiFinancialAnalyzer.detect_column_mapping(df, columns)

# Example output:
{
    "date_column": "Transaction Date",
    "income_column": "Revenue",
    "expense_column": "Cost",
    "amount_column": "Amount",
    "category_column": "Type",
    "confidence": "high"
}
```

### 2. Data Processing
The system then:
- Renames columns to standard names
- Cleans and validates data
- Handles missing values
- Creates income/expense columns if needed

### 3. AI Analysis
Gemini AI provides:
- Custom insights for your specific data
- Recommendations based on patterns
- Risk assessment
- Growth opportunities

## Example Use Cases

### Case 1: Simple Transaction File
```csv
Date,Amount,Type
2024-01-01,5000,Income
2024-01-02,-1200,Rent
2024-01-03,-300,Supplies
```
✓ AI detects: Date, Amount (splits into income/expenses based on Type)

### Case 2: Detailed Financial Data
```csv
Period,Revenue,Expenses,Category
Jan 2024,15000,8000,Operations
Feb 2024,18000,9000,Operations
```
✓ AI detects: Period as date, Revenue, Expenses

### Case 3: Mixed Format
```csv
Transaction_Date,Debit,Credit,Description
2024-01-01,0,5000,Client Payment
2024-01-02,1200,0,Office Rent
```
✓ AI detects: Transaction_Date as date, Credit as income, Debit as expenses

## Fallback Mechanism

If Gemini AI is unavailable or the API key is invalid, the system automatically falls back to:
- Pattern-based column detection
- Keyword matching
- Standard financial data assumptions

This ensures your application works even without AI!

## Testing

### Test the Gemini Connection:
```python
from backend.gemini_helper import test_gemini_connection

success, message = test_gemini_connection()
print(f"Gemini API Status: {'Connected' if success else 'Failed'}")
print(f"Message: {message}")
```

### Test with Sample Data:
1. Upload any CSV file with financial data
2. Check the server logs for: `Detected column mapping: {...}`
3. Verify the analysis results

## Troubleshooting

### Error: "API key not configured"
- Solution: Update `GEMINI_API_KEY` in `gemini_helper.py`

### Error: "API quota exceeded"
- Solution: Gemini has free tier limits. Upgrade your plan or wait for quota reset

### Error: "Unable to parse JSON from AI"
- Solution: This is handled automatically. The system falls back to pattern matching.

### Data not being detected correctly:
- The AI usually gets it right, but if not, check that:
  - Your CSV has headers
  - Numerical values are formatted correctly
  - Dates are recognizable

## API Rate Limits

Gemini API Free Tier:
- 60 requests per minute
- 1,500 requests per day
- Perfect for small to medium applications

If you need more:
- Visit: https://ai.google.dev/pricing
- Upgrade to paid tier for higher limits

## Security Notes

⚠️ **Important:**
1. Never commit API keys to public repositories
2. Use environment variables in production
3. Rotate keys periodically
4. Monitor API usage in Google Cloud Console

## Next Steps

1. ✅ API key is configured
2. ✅ Backend server is running
3. ✅ Frontend is ready
4. 📤 **Try uploading a file!**

The system will now work with ANY CSV structure - the AI will figure it out!

## Need Help?

- Gemini API Docs: https://ai.google.dev/docs
- Get API Key: https://makersuite.google.com/app/apikey
- Check usage: https://console.cloud.google.com/

---

**Status:** ✅ Gemini AI Integration Complete!
**Your Application:** Now supports ANY CSV/Excel file format!
