import pandas as pd
import os
from datetime import datetime

class DataProcessor:
    def __init__(self):
        self.download_dir = 'downloads'
        if not os.path.exists(self.download_dir):
            os.makedirs(self.download_dir)
    
    def save_data(self, data, data_type, format_type='csv'):
        if not data:
            return None
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{data_type}_{timestamp}.{format_type}"
        filepath = os.path.join(self.download_dir, filename)
        
        try:
            df = pd.DataFrame(data)
            if format_type == 'csv':
                df.to_csv(filepath, index=False, encoding='utf-8')
            elif format_type == 'xlsx':
                df.to_excel(filepath, index=False, sheet_name='Data')
            elif format_type == 'json':
                df.to_json(filepath, orient='records', indent=2)
            return filename
        except:
            return None