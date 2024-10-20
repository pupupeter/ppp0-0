# -*- coding: utf-8 -*-
"""國立中山大學附屬國光高級中學_310085_楊森宇.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1drN35l4adubRM4FnHOk5c5DCC0M3aORn
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

# 讀取CSV資料
df = pd.read_csv('/content/觀光遊憩據點按縣市及遊憩據點交叉分析.csv')

# 縣市名稱替換
county_name_mapping = {
   '金門縣': 'Kinmen',
   '連江縣': 'Lianjiang',
   '澎湖縣': 'Penghu',
   '臺東縣': 'Taitung'
}

# 將縣市名稱替換
df['縣市'] = df['縣市'].replace(county_name_mapping)

# 將 '小計' 列中的非數字數據轉換為 NaN，並且將列轉為浮點數
df['小計'] = pd.to_numeric(df['小計'], errors='coerce')

# 刪除 '小計' 列中為 NaN 的行
df = df.dropna(subset=['小計'])

# 計算每個縣市的最大值和中位數
county_summary = df.groupby('縣市')['小計'].agg(['max', 'median'])

# 繪製箱型圖
plt.figure(figsize=(12, 6))
plt.boxplot(
    [df[df['縣市'] == county]['小計'] for county in county_name_mapping.values()],
    labels=county_name_mapping.values()
)
plt.xlabel('County', fontsize=14)
plt.ylabel('Tourists', fontsize=14)
plt.grid(axis='y')
plt.xticks(rotation=45)

# 標註中位數和最大值
for idx, (i, row) in enumerate(county_summary.iterrows(), start=1):
    median = row['median']
    max_value = row['max']

    # 標註中位數和最大值
    plt.text(idx, median, f'Median: {median}', ha='center', va='bottom', fontsize=10, color='black')
    plt.text(idx, max_value, f'Max: {max_value}', ha='center', va='bottom', fontsize=10, color='blue')

# 顯示圖表
plt.tight_layout()
# 保存圖表
plt.savefig('001.jpg')
plt.clf()

#-------------------------------------------------------------------------------



import json

# 假設已讀取 JSON 檔案
with open('HotelList.json', 'r', encoding='utf-8-sig') as f:
    data = json.load(f)

# 取得旅館列表
hotels = data['Hotels']

# 查詢函式
def search_hotels(city, service_info, budget):
    # 根據縣市篩選
    filtered_hotels = [hotel for hotel in hotels if hotel['PostalAddress']['City'] == city]
    if not filtered_hotels:
        print("未找到符合地點的旅館/民宿")
        return

    # 根據特殊需求篩選
    if service_info:
        filtered_hotels = [hotel for hotel in filtered_hotels if service_info in hotel['ServiceInfo']]
        if not filtered_hotels:
            print("未找到符合地點和特殊需求的旅館/民宿")
            return

    # 根據價位範圍篩選
    filtered_hotels = [hotel for hotel in filtered_hotels if hotel['LowestPrice'] <= budget <= hotel['CeilingPrice']]
    if not filtered_hotels:
        print("未找到符合預算的旅館/民宿")
        return

    # 印出前5筆符合條件的旅館資訊
    for hotel in filtered_hotels[:5]:
        print(f"HotelName: {hotel['HotelName']}, "
              f"LowestPrice: {hotel['LowestPrice']}, "
              f"CeilingPrice: {hotel['CeilingPrice']}, "
              f"Description: {hotel['Description']}, "
              f"PostalAddress.Town: {hotel['PostalAddress']['Town']}, "
              f"PostalAddress.StreetAddress: {hotel['PostalAddress']['StreetAddress']}")

# 主程式
while True:
    # 輸入縣市
    city = input("請輸入縣市: ")
    if not city:
        break

    # 輸入特殊需求 (可選)
    service_info = input("請輸入特殊需求(可輸入無或留空): ")
    if service_info.lower() == '無' or not service_info:
        service_info = None

    # 輸入價位範圍
    try:
        budget = int(input("請輸入價位(範圍1000-20000): "))
        if budget < 1 or budget > 20000:
            raise ValueError
    except ValueError:
        print("請輸入有效的價位範圍(1~20000)")
        continue

    # 執行查詢
    search_hotels(city, service_info, budget)
    break

"""HotelList.json"""