# -*- coding: utf-8 -*-
"""Untitled3.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1E9qOIj_vYaapYQp3wD-l-eM6zQpcGdGZ
"""

# 匯入必要的套件
import pandas as pd
import matplotlib.pyplot as plt
import warnings

# 忽略 FutureWarning
warnings.filterwarnings("ignore", category=FutureWarning)

# 讀取資料 (CSV 和 JSON)
hotel_csv = pd.read_csv('HotelList.csv')
hotel_json = pd.read_json('HotelList.json')

# 將 CSV 和 JSON 合併
data = pd.concat([hotel_csv, hotel_json], ignore_index=True)

# 保留需要的欄位 (名稱、價格、地址等)
columns_to_keep = ['HotelName', 'City', 'LowestPrice', 'CeilingPrice',
                   'Description', 'PostalAddressTown', 'PostalAddress', 'StreetAddress']
data = data[columns_to_keep]

# 將價格欄位轉換為數字格式，避免處理錯誤
data['LowestPrice'] = pd.to_numeric(data['LowestPrice'], errors='coerce')
data['CeilingPrice'] = pd.to_numeric(data['CeilingPrice'], errors='coerce')

# 去除空值或無效資料
data = data.dropna(subset=['LowestPrice', 'CeilingPrice'])

# 繪製箱型圖 (按城市分組的價格範圍)
plt.figure(figsize=(10, 6))
boxplot = data.boxplot(column=['LowestPrice', 'CeilingPrice'], by='City', grid=False)

# 標註 Max 和 Median
for i, row in data.groupby('City'):
    max_price = row['CeilingPrice'].max()
    median_price = row['CeilingPrice'].median()
    plt.text(i, max_price, f'Max: {int(max_price)}', ha='center', color='blue')
    plt.text(i, median_price, f'Median: {int(median_price)}', ha='center', color='black')

# 設定圖表標題和軸標籤
plt.title('Hotel Price Range by City')
plt.suptitle('')  # 移除預設標題
plt.xlabel('City')
plt.ylabel('Price')

# 儲存圖表為 JPG 格式，且按照作業要求命名為 '001.jpg'
plt.savefig('001.jpg', format='jpg')

# 顯示訊息，確認輸出成功
print("圖表已成功儲存為 001.jpg")

# 輸出資料範例（可根據需求調整輸出格式）
print("\n數據範例輸出：")
print(data.head())