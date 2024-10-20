# -*- coding: utf-8 -*-
"""Untitled1.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1D9tuQg2qHiTzHbsAE_wDCkSlqOQUsYqb
"""

import seaborn as sns
import warnings
import pandas as pd
import matplotlib.pyplot as plt
import json
from tabulate import tabulate
from google.colab import files


warnings.filterwarnings("ignore", category=FutureWarning)

df = pd.read_csv('觀光遊憩據點按縣市及遊憩據點交叉分析.csv')



county_name_mapping = {
    '金門縣': 'Kinmen',
    '臺東縣': 'Taitung',
    '澎湖縣': 'Penghu',
    '連江縣': 'Lianjiang'
}

df['縣市'] = df['縣市'].map(county_name_mapping)

月份欄位 = df.columns[4:-1]


for 欄位 in 月份欄位:
    df[欄位] = pd.to_numeric(df[欄位].str.extract(r'(\d+)', expand=False), errors='coerce')
    if df[欄位].isnull().any():
        print(f"欄位 {欄位} 有 NaN 值")

df['總和'] = df[月份欄位].sum(axis=1)
縣市總和 = df.groupby('縣市')['總和'].agg(['median', 'max']).reset_index()

plt.figure(figsize=(12, 6))
sns.boxplot(x='縣市', y='總和', data=df, order=list(county_name_mapping.values()), showfliers=False)


for i, 縣市 in enumerate(county_name_mapping.values()):
    最大值 = 縣市總和.loc[縣市總和['縣市'] == 縣市, 'max'].values[0]
    中位數 = 縣市總和.loc[縣市總和['縣市'] == 縣市, 'median'].values[0]

    plt.text(i, 最大值, f'Max: {int(最大值)}', ha='center', va='bottom', fontsize=10, color='blue')
    plt.text(i, 中位數, f'Median: {int(中位數)}', ha='center', va='top', fontsize=10, color='black')

plt.xlabel('County', fontsize=14)
plt.ylabel('Tourists', fontsize=14)
plt.grid(axis='y')
plt.xticks(rotation=45)
plt.tight_layout()

plt.savefig('001.jpg')
plt.clf()


# 讀取旅館資料
with open('HotelList.json', 'r', encoding='utf-8-sig') as file:
    data = json.load(file)

hotels_df = pd.json_normalize(data['Hotels'])

# 詢問篩選條件
user_input_city = input("請輸入城市名稱（例如：臺東縣）：").strip()

# 檢查是否有符合地點的旅館
matching_hotels_by_city = hotels_df[hotels_df['PostalAddress.City'] == user_input_city]
if matching_hotels_by_city.empty:
    print("未找到符合地點的旅館/民宿")
else:
    user_input_service1 = input("請輸入想要的服務資訊關鍵字（例如：自行車友善），或按 Enter 或輸入 '無' 跳過：").strip()

    # 篩選符合特殊需求的旅館
    matching_hotels_after_service = matching_hotels_by_city
    if user_input_service1.lower() != '無' and user_input_service1 != '':
        matching_hotels_after_service = matching_hotels_by_city[
            matching_hotels_by_city['ServiceInfo'].str.contains(user_input_service1, case=False, na=False)]
        if matching_hotels_after_service.empty:
            print("未找到符合地點和特殊需求的旅館/民宿")

    # 若前面篩選有結果，則詢問預算
    if not matching_hotels_after_service.empty:
        user_input_budget = int(input("請輸入預算（例如：2500）是一整數範圍為1~20000："))

        # 篩選符合預算的旅館
        matching_hotels_by_budget = matching_hotels_after_service[
            (matching_hotels_after_service['LowestPrice'] <= user_input_budget) &
            (matching_hotels_after_service['CeilingPrice'] >= user_input_budget)
        ]
        if matching_hotels_by_budget.empty:
            print("未找到符合預算的旅館/民宿")
        else:
            print("在", user_input_city, "的符合所有條件的旅館有：")
            print(tabulate(matching_hotels_by_budget[['HotelName', 'LowestPrice', 'CeilingPrice', 'Description', 'PostalAddress.Town', 'PostalAddress.StreetAddress']], headers='keys', tablefmt='psql'))

