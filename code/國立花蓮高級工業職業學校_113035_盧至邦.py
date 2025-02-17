# -*- coding: utf-8 -*-
"""國立花蓮高級工業職業學校_113035_盧至邦

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1jWsQSVW1ojW3E1EL08CCB4hTdcNAuSCc
"""

import pandas as pd
import json

# 步驟1: 讀取 JSON 檔案
with open('HotelList.json', 'r', encoding='utf-8-sig') as file:
    data = json.load(file)

# 步驟2: 將 JSON 轉換為 DataFrame
hotels_df = pd.json_normalize(data['Hotels'])

# 步驟3: 確保價格是數值類型
hotels_df['LowestPrice'] = pd.to_numeric(hotels_df['LowestPrice'], errors='coerce')
hotels_df['CeilingPrice'] = pd.to_numeric(hotels_df['CeilingPrice'], errors='coerce')

# 進行篩選操作
def search_hotels():
    # 第一次輸入：縣市篩選
    city = input("").strip()

    # 確認是否有 'PostalAddress.City' 欄位，並進行篩選
    if 'PostalAddress.City' not in hotels_df.columns:
        print("未找到符合地點的旅館/民宿")
        return

    city_filtered_df = hotels_df[hotels_df['PostalAddress.City'] == city]

    if city_filtered_df.empty:
        print("未找到符合地點的旅館/民宿")
        return

    # 第二次輸入：特殊需求篩選
    special_request = input("").strip()
    if special_request and special_request.lower() != '無':
        special_filtered_df = city_filtered_df[city_filtered_df['ServiceInfo'].str.contains(special_request, case=False, na=False)]
        if special_filtered_df.empty:
            print("未找到符合地點和特殊需求的旅館/民宿")
            return
    else:
        special_filtered_df = city_filtered_df

    # 第三次輸入：價位篩選
    price_range = input("").strip()

    try:
        price_range = int(price_range)
        if price_range < 1 or price_range > 20000:
            raise ValueError
    except ValueError:
        print("未找到符合預算的旅館/民宿")
        return

    price_filtered_df = special_filtered_df[
        (special_filtered_df['LowestPrice'] <= price_range) &
        (special_filtered_df['CeilingPrice'] >= price_range)
    ]

    if price_filtered_df.empty:
        print("未找到符合預算的旅館/民宿")
        return

    # 輸出前5筆結果
    result_df = price_filtered_df[['HotelName', 'LowestPrice', 'CeilingPrice', 'Description',
                                   'PostalAddress.Town', 'PostalAddress.StreetAddress']].head(5)

    print(result_df.to_string(index=False))

# 呼叫函數執行查詢
search_hotels()

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings

# 忽略 FutureWarning
warnings.filterwarnings("ignore", category=FutureWarning)

# 1. 讀取 CSV 檔案
file_path = '觀光遊憩據點按縣市及遊憩據點交叉分析.csv'  # 更新檔案路徑
data = pd.read_csv(file_path)

# 2. 資料清理
# 篩選出需要的縣市 (Max 篩選條件)
cities_of_interest = ['臺東縣', '澎湖縣', '金門縣', '連江縣']
filtered_data = data[data['縣市'].isin(cities_of_interest)]  # Max 篩選條件：篩選出目標縣市

# 為防止中文亂碼出現，將縣市的中文名稱替換為英文名稱 (Medium 篩選條件)
county_name_mapping = {
    '金門縣': 'Kinmen',
    '臺東縣': 'Taitung',
    '澎湖縣': 'Penghu',
    '連江縣': 'Lianjiang'
}
# 將縣市名稱替換為英文名稱
filtered_data['縣市'] = filtered_data['縣市'].replace(county_name_mapping)

# 3. 數據整理
# 將所有年月的觀光人數加總 (Max 數據處理)
months_columns = filtered_data.columns[2:-1]  # 從第三列到最後一列（不包括小計）

# 將 months_columns 轉換為數值型別並進行加總 (Medium 數據處理)
for col in months_columns:
    filtered_data[col] = pd.to_numeric(filtered_data[col], errors='coerce')

filtered_data['總觀光人數'] = filtered_data[months_columns].sum(axis=1)  # Max 數據處理：加總每列的觀光人數

# 4. 繪製箱型圖
plt.figure(figsize=(12, 6))
sns.boxplot(data=filtered_data, x='縣市', y='總觀光人數', order=['Kinmen', 'Lianjiang', 'Penghu', 'Taitung'])
plt.title('')  # 將標題設為空白
plt.xlabel('County', fontsize=14)
plt.ylabel('Tourists', fontsize=14)
plt.grid(axis='y')
plt.xticks(rotation=45)

# 計算各縣市的中位數和最大值
median_values = filtered_data.groupby('縣市')['總觀光人數'].median()  # Medium：中位數
max_values = filtered_data.groupby('縣市')['總觀光人數'].max()  # Max：最大值

# 標註Median
median_values = filtered_data.groupby('縣市')['總觀光人數'].median()
for i, city in enumerate(median_values.index):
    plt.text(i, median_values[city], f'Median: {median_values[city]:.2f}', color='black', ha='center')

# 標註Max
max_values = filtered_data.groupby('縣市')['總觀光人數'].max()
for i, city in enumerate(max_values.index):
    plt.text(i, max_values[city], f'Max: {max_values[city]:.2f}', color='blue', ha='center', va='bottom')

# 儲存圖表
plt.tight_layout()
plt.savefig('updated_boxplot.jpg', format='jpg')
plt.clf()