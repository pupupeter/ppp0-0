# -*- coding: utf-8 -*-
"""國立羅東高級工業職業學校_218202_王博甫

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1w7IMlsok664WE1JrrTVZ_xTwdz4x7WGy
"""

import pandas as pd
import matplotlib.pyplot as plt

# 讀取 CSV 檔案
df = pd.read_csv('myExpenses1.csv')

# 將 'Date' 欄位轉換為日期時間格式, 指定日期格式為 '%d/%m/%Y'
df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y') # Specify the correct date format

# 找出消費金額前十高的品項
top10_items = df.groupby('Item')['Amount'].sum().sort_values(ascending=False).head(10)

# 生成直方圖
plt.bar(top10_items.index, top10_items.values)
plt.xlabel('Item')
plt.ylabel('Total Amount spent')
plt.savefig('001.jpg')  # 匯出直方圖
plt.clf()
plt.close()

# 計算星期一到星期日的消費比例
weekday_spending = df.groupby('day')['Amount'].sum()
weekday_spending_ratio = (weekday_spending / weekday_spending.sum() * 100).astype(int)

# 生成圓餅圖
weekday_labels = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
plt.pie(weekday_spending_ratio, labels=weekday_labels[::-1], counterclock=False, autopct='%d%%')  # 添加比例
plt.savefig('002.jpg')  # 匯出圓餅圖
plt.clf()
plt.close()

# 列印消費金額最高的品項以及金額
print(f'Item with the highest spending is {top10_items.index[0]}')
print(f'Total amount spent is {top10_items.values[0]}')

print()  # 空行

# 分別找出星期一到星期日消費最高的日子，並列印出日期
for day in weekday_labels:
    max_spending_date = df[df['day'] == day]['Amount'].idxmax()
    print(f'Highest spending day on {day} is {df.loc[max_spending_date, "Date"].strftime("%Y-%m-%d")}')  # 格式化日期

highest_item = item_totals.idxmax()
highest_amount = item_totals.max()
print(f'消費最高的品項名稱: {highest_item}, 金額: {highest_amount}')

# 將日期轉換為日期格式
data['Date'] = pd.to_datetime(data['Date'], format='%d/%m/%Y')

# 添加星期幾列
data['Weekday'] = data['Date'].dt.day_name()

# 計算每個星期的消費總額
weekly_totals = data.groupby('Weekday')['Amount'].sum()

# 繪製圓餅圖
plt.figure(figsize=(8, 8))
weekly_totals.plot(kind='pie', autopct='%1.1f%%', startangle=90)
plt.title('星期一到日的消費比例')
plt.ylabel('')
plt.savefig('weekly_expense_distribution_pie_chart.jpg')
plt.clf()

max_days = data.loc[data.groupby('Weekday')['Amount'].idxmax()]

for index, row in max_days.iterrows():
  formatted_date = row['Date'].strftime('%Y-%m-%d')
  print(f"星期 {row['Weekday']} 消費最高的日期: {formatted_date}, 金額: {row['Amount']}")

