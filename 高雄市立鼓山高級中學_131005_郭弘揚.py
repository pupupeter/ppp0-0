# -*- coding: utf-8 -*-
"""HW3

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1sClKq46xILxang5kf6P9Ue_-w0g7XTw2
"""

import seaborn as sns
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)
import pandas as pd
import matplotlib.pyplot as plt

# 讀取 CSV 檔案
 df = pd.read_csv('觀光遊憩據點按縣市及遊憩據點交叉分析.csv')

# 定義縣市名稱映射
county_name_mapping = {
    '金門縣': 'Kinmen',
    '連江縣': "Lianjiang",
    '澎湖縣': 'Penghu',
    '臺東縣': 'Taitung',

}

# 將縣市中文名稱替換為英文名稱
df['縣市'] = df['縣市'].map(county_name_mapping)

# 選擇月份欄位並計算總和
月份欄位 = df.columns[4:-1]  # 從第五欄到倒數第二欄

# 將月份欄位轉換為數值類型，處理日期格式
for 欄位 in 月份欄位:
    # 嘗試提取月份並轉換為數值
    df[欄位] = pd.to_numeric(df[欄位].str.extract(r'(\d+)', expand=False), errors='coerce')

# 按照縣市分組並計算總和、中位數和最大值
df['總和'] = df[月份欄位].sum(axis=1)
縣市總和 = df.groupby('縣市')['總和'].agg(['median', 'max']).reset_index()  # 直接計算中位數和最大值

# 使用 seaborn 生成箱型圖
plt.figure(figsize=(12, 6))
# 使用英文縣市名稱繪製箱型圖，並使用 showfliers=False 隱藏離群值
sns.boxplot(x='縣市', y='總和', data=df, order=list(county_name_mapping.values()), showfliers=False)
# 定義 stats 變數，將縣市作為索引
stats = 縣市總和.set_index('縣市')
# 標註最大值、中位數，使用英文縣市名稱
#箱形圖算中位數、最大數的語法
for i, county in enumerate(stats.index):
    plt.text(i, stats['median'][county], f'Median: {int(stats["median"][county])}',
             ha='center', va='bottom', fontsize=10, color='black')
    plt.text(i, stats['max'][county], f'Max: {int(stats["max"][county])}',
             ha='center', va='bottom', fontsize=10, color='blue')
# 設定圖表樣式，使用英文標籤
plt.xlabel('County', fontsize=14)
plt.ylabel('Tourists', fontsize=14)
plt.grid(axis='y')
plt.xticks(rotation=45)  # 旋轉 x 軸標籤
plt.tight_layout()

# 儲存圖表
plt.savefig('001.jpg')
plt.clf()
plt.close()




import json
import pandas as pd

with open('HotelList.json', 'r', encoding='utf-8-sig') as file:
    data = json.load(file)

hotels_df = pd.json_normalize(data['Hotels'])
print('請輸入城市名稱（例如：臺東縣）\n請輸入想要的服務資訊關鍵字（例如：自行車友善）\n請輸入預算（例如：2500）')
# 詢問篩選條件
user_input_city = input()

# 1. 檢查是否有符合地點的旅館
matching_hotels_by_city = hotels_df[hotels_df['PostalAddress.City'] == user_input_city]
if matching_hotels_by_city.empty:
    print("未找到符合地點的旅館/民宿")
else:
    user_input_service1 = input()

    # 篩選符合特殊需求的旅館，若跳過則使用原始結果
    matching_hotels_after_service = matching_hotels_by_city
    if user_input_service1.lower() != '無' and user_input_service1 != '':
        matching_hotels_after_service = matching_hotels_by_city[
            matching_hotels_by_city['ServiceInfo'].str.contains(user_input_service1,case=False, na=False)]
        from tabulate import tabulate
        if matching_hotels_after_service.empty:
            print("未找到符合地點和特殊需求的旅館/民宿")

    # 若前面篩選有結果，則繼續詢問預算
    if not matching_hotels_after_service.empty:
        user_input_budget = int(input())

        # 篩選符合預算的旅館
        matching_hotels_by_budget = matching_hotels_after_service[
            (matching_hotels_after_service['LowestPrice'] <= user_input_budget) &
            (matching_hotels_after_service['CeilingPrice'] >= user_input_budget)
        ]
        if matching_hotels_by_budget.empty:
            print("未找到符合預算的旅館/民宿")
        else:
            print("在", user_input_city, "的符合所有條件的旅館有：")
            print(matching_hotels_by_budget[['HotelName', 'LowestPrice', 'CeilingPrice', 'Description', 'PostalAddress.Town', 'PostalAddress.StreetAddress']].head(5).to_string(index=False))