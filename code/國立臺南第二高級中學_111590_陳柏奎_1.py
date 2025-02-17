# -*- coding: utf-8 -*-
"""「Taiwan Trip.ipynb」的副本

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1s-SwAWBHObJSLRb6pwjBmvckRI4K23v5
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings

# 忽略 FutureWarning
warnings.filterwarnings("ignore", category=FutureWarning)

# 讀取 CSV 文件
file_path = '觀光遊憩據點按縣市及遊憩據點交叉分析.csv'
df = pd.read_csv(file_path)

# 清理數據，移除無關的欄位（如 'Unnamed: 1' 和 'Unnamed: 3'）
df_clean = df.drop(columns=['Unnamed: 1', 'Unnamed: 3'])

# 只保留月份相關的列，並轉換為數字類型
months_columns = df_clean.columns[4:-1]  # 從第 5 列到倒數第 2 列，排除 '小計'
df_clean[months_columns] = df_clean[months_columns].apply(pd.to_numeric, errors='coerce')

# 縣市名稱的對應字典
county_name_mapping = {
    '金門縣': 'Kinmen',
    '臺東縣': 'Taitung',
    '澎湖縣': 'Penghu',
    "連江縣": "Lianjiang"
}

# 替換縣市名稱
df_clean['縣市'] = df_clean['縣市'].replace(county_name_mapping)

# 按縣市分組，並加總每個月的觀光人數
df_grouped = df_clean.groupby('縣市')[months_columns].sum()

# 轉置資料框，使得月份成為 X 軸，縣市成為不同的數據系列
df_grouped_T = df_grouped.T

# 計算統計數據
stats = df_grouped_T.describe().T[['max', '50%']].rename(columns={'50%': 'median'})

# 繪製箱型圖
plt.figure(figsize=(12, 6))
sns.boxplot(data=df_grouped_T)

# 標註中位數和最大值
for i, county in enumerate(stats.index):
    plt.text(i, stats['median'][county], f'Median: {int(stats["median"][county])}',
             ha='center', va='bottom', fontsize=10, color='black')
    plt.text(i, stats['max'][county], f'Max: {int(stats["max"][county])}',
             ha='center', va='bottom', fontsize=10, color='blue')

# 設置標題和標籤
plt.title('不同縣市的每月觀光人數分布', fontsize=16)
plt.xlabel('County', fontsize=14)
plt.ylabel('Tourists', fontsize=14)

# 添加網格、旋轉 X 軸標籤、緊湊排版
plt.grid(axis='y')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('001.jpg')
plt.clf()

import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
from tabulate import tabulate

warnings.filterwarnings("ignore", category=FutureWarning)

# 讀取旅館資料
with open('HotelList.json', 'r', encoding='utf-8-sig') as file:
    data = json.load(file)

# 將資料轉成DataFrame
hotels_df = pd.json_normalize(data['Hotels'])

# 假設用戶輸入的城市
user_input_city = input()
matching_hotels = hotels_df[hotels_df['PostalAddress.City'] == user_input_city]

if matching_hotels.empty:
    print("未找到符合地點的旅館/民宿")
else:
    # 詢問是否有特殊需求
    user_input_special_condition = input("")

    if user_input_special_condition.lower() and user_input_special_condition.lower() != '無':
        matching_hotels = matching_hotels[matching_hotels['ServiceInfo'].str.contains(user_input_special_condition, case=False, na=False)]

    if matching_hotels.empty:
        print("未找到符合地點和特殊需求的旅館/民宿")
    else:
        user_input_budget = int(input(""))
        final_matching_hotels = matching_hotels[(matching_hotels['LowestPrice'] <= user_input_budget) & (matching_hotels['CeilingPrice'] >= user_input_budget)]

        if not final_matching_hotels.empty:
            # 使用 Pandas 內建方法輸出前五個結果
            columns_to_display = ['HotelName', 'LowestPrice', 'CeilingPrice', 'Description', 'PostalAddress.Town', 'PostalAddress.StreetAddress']
            print(final_matching_hotels[columns_to_display].head(5).to_string(index=False))
        else:
            print("未找到符合預算的旅館/民宿")