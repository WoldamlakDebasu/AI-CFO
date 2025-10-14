import pandas as pd
import sys
sys.path.insert(0, '/workspaces/AI-CFO')

from app.models import FinancialData

# Create a mock file object
class MockFile:
    def __init__(self, filepath):
        self.filepath = filepath
        self.filename = filepath.split('/')[-1]
        with open(filepath, 'rb') as f:
            self.content = f.read()
        self.pos = 0
    
    def read(self, size=-1):
        if size == -1:
            result = self.content[self.pos:]
            self.pos = len(self.content)
        else:
            result = self.content[self.pos:self.pos + size]
            self.pos += len(result)
        return result
    
    def seek(self, pos):
        self.pos = pos
        
    def tell(self):
        return self.pos

# Test the file
try:
    mock_file = MockFile('/workspaces/AI-CFO/test_upload.csv')
    
    # Read directly with pandas first
    df = pd.read_csv('/workspaces/AI-CFO/test_upload.csv')
    print("=== Direct Pandas Read ===")
    print(f"Columns: {df.columns.tolist()}")
    print(f"Shape: {df.shape}")
    print(f"\nFirst few rows:\n{df.head()}")
    
    # Now test with FinancialData class
    print("\n\n=== Testing with FinancialData Class ===")
    financial_data = FinancialData(mock_file)
    print(f"Columns after processing: {financial_data.df.columns.tolist()}")
    print(f"Shape: {financial_data.df.shape}")
    
    # Test cash flow
    print("\n=== Testing Cash Flow ===")
    cash_flow = financial_data.get_cash_flow()
    print(f"Cash Flow Result: {cash_flow}")
    
except Exception as e:
    print(f"ERROR: {str(e)}")
    import traceback
    traceback.print_exc()
