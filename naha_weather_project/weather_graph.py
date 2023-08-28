import json
from collections import Counter
import matplotlib.pyplot as plt

with open("naha_weekend_weather_data.json", "r") as file:
    data = json.load(file)

# 月ごとの天気の出現回数をカウント
monthly_weather_counter = {}
for entry in data:
    year_month = entry["year"] + "-" + entry["month"]
    if year_month not in monthly_weather_counter:
        monthly_weather_counter[year_month] = Counter()
    monthly_weather_counter[year_month][entry["weather_3pm"]] += 1

# 各月の最も一般的な天気とその出現回数を取得
most_common_weather = {month: weather.most_common(1)[0] for month, weather in monthly_weather_counter.items()}

# グラフの描画
months = list(most_common_weather.keys())
weather_counts = [weather[1] for weather in most_common_weather.values()]
weather_labels = [weather[0] for weather in most_common_weather.values()]

plt.figure(figsize=(15, 7))
plt.bar(months, weather_counts, color=['blue' if label == "晴れ" else 'gray' if label == "曇り" else 'green' for label in weather_labels])
plt.xlabel('Month')
plt.ylabel('Count')
plt.title('Most Common Weather Each Month')
plt.xticks(rotation=45)

# 天気ラベルを追加
for i, (count, label) in enumerate(zip(weather_counts, weather_labels)):
    plt.text(i, count+0.2, label, ha='center')

plt.tight_layout()
plt.show()
plt.savefig("weather_graph.png")