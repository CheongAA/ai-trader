import os
import pandas as pd

def save_to_excel(data, file_name="crypto_data.xlsx"):
    """데이터를 엑셀 파일로 저장"""
    print(data)
    if data is None:
        print("No data to save")
        return
    
    # DataFrame으로 변환
    df = pd.DataFrame(data)
    
    # 엑셀 파일로 저장
    file_path = os.path.join(os.getcwd(), file_name)
    try:
        df.to_excel(file_path, index=False, sheet_name="Crypto Data")
        print(f"Data successfully saved to {file_path}")
    except Exception as e:
        print(f"Error saving data to Excel: {e}")
