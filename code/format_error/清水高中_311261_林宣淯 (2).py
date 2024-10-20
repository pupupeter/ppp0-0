# -*- coding: utf-8 -*-
"""清水高中_311261_林宣淯

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1IX4bnDUmsNyo6FideubAVDYXarX5Xhac
"""

import pandas as pd
import matplotlib.pyplot as plt
import json
import warnings

warnings.filterwarnings("ignore", category=FutureWarning)

# 讀取 CSV 檔案
def search_hotels(city, service, price_range):
    # 篩選符合條件的旅館，並返回結果
    filtered_hotels = [hotel for hotel in hotels if hotel['city'] == city and service in hotel['services'] and price_range[0] <= hotel['price'] <= price_range[1]]
    return filtered_hotels

# ...

# 獲取用戶輸入
city = input("請輸入城市：")
service = input("請輸入特殊需求：")
price_range = [int(x) for x in input("請輸入價格範圍 (最小值-最大值)：").split('-')]

# 搜尋旅館
results = search_hotels(city, service, price_range)

# 輸出結果
if results:
    for i, hotel in enumerate(results):
        print(f"第{i+1}間旅館：")
        print(f"飯店名稱：{hotel['name']}")
        # ...
else:
    print("未找到符合條件的旅館")

# 分組計算觀光人數並繪製箱型圖
for county in df['縣市'].unique():
    county_data = df[df['縣市'] == county]
    plt.boxplot(county_data.groupby('月份')['觀光人數'].sum())
    plt.savefig(f'{county}.jpg', bbox_inches='tight')
    plt.clf()

# 讀取 JSON 檔案
with open('HotelList.json', 'r') as f:
    hotel_data = json.load(f)

# 互動式查詢
while True:
    city = input('請輸入城市：')
    service = input('請輸入特殊需求：')
    price_range = input('請輸入價格範圍 (1-20000)：')

    try:
        price_range = int(price_range)
        if price_range < 1 or price_range > 20000:
            raise ValueError
    except ValueError:
        print('價格範圍輸入錯誤，請輸入1-20000之間的整數')
        continue

    # 篩選符合條件的旅館
    filtered_hotels = [hotel for hotel in hotel_data if hotel['City'] == city and service in hotel['ServiceInfo'] and hotel['LowestPrice'] <= price_range <= hotel['CeilingPrice']]

    if not filtered_hotels:
        print('未找到符合地點和特殊需求的旅館/民宿')
        break

    # 輸出前5筆結果
    for i, hotel in enumerate(filtered_hotels[:5]):
        print(f"第{i+1}間旅館：")
        print(f"飯店名稱：{hotel['HotelName']}")
        print(f"最低價格：{hotel['LowestPrice']}")
        print(f"最高價格：{hotel['CeilingPrice']}")
        print(f"描述：{hotel['Description']}")
        print(f"郵遞區號：{hotel['PostalAddress']['Town']}")
        print(f"街道地址：{hotel['PostalAddress']['StreetAddress']}")
        print()

    # 詢問是否繼續查詢
    if input('是否繼續查詢 (y/n)？') != 'y':
        break