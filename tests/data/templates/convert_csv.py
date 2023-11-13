import pandas as pd
import os

for filename in os.listdir('.'):
    if filename.endswith('.xlsx'):
        os.remove(filename)
        df = pd.read_excel(filename)
        filename = filename.lower()
        filename = filename.replace(' ', '-')
        filename = filename.replace('.xlsx', '.csv')
        df.to_csv(filename, index=False)
