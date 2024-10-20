# -*- coding: utf-8 -*-
"""高雄市仁武高級中學 1132160  許昱佑.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/16Y3btNgI3Q0XI9X9mo1Gn89lv1iRg5tg
"""

def calculate_weighted_grade(grades, weights):
    if len(grades) != len(weights):
        raise ValueError("成绩和权重的数量必须相同")

    if not (0.99 <= sum(weights) <= 1.01):  # 确保权重总和为1
        raise ValueError("权重的总和必须为 1")

    weighted_sum = sum(grade * weight for grade, weight in zip(grades, weights))
    return weighted_sum

# 初始化五科成绩和科目名称
grades = [0] * 5
subjects = ["国", "英", "数", "自", "社"]
weights = [0.2, 0.25, 0.15, 0.3, 0.1]  # 权重

# 输入成绩并检查是否超过100
for i in range(5):
    while True:
        score = float(input(f"请输入{subjects[i]}科的成绩："))
        if 0 <= score <= 100:  # 检查成绩是否在有效范围内
            grades[i] = score
            break
        else:
            print("成绩必须在 0 到 100 之间，请重新输入。")

# 计算加权成绩
weighted_grade = calculate_weighted_grade(grades, weights)

# 输出加权成绩
print(f"加权成绩: {weighted_grade:.2f}")
2