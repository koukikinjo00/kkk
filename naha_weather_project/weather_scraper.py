import requests
from bs4 import BeautifulSoup
import calendar
import json

# 対象のURL
base_url = "https://weather.goo.ne.jp/past/936/{year}{month}00/"

def extract_weather_data(url, year, month):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    table = soup.find("table", class_="t01 past01 mb10")

    # 日付の取得
    days = [td.get_text() for td in table.select('tr td.day') if td.get_text() != '-']
    
    # 15時の天気情報の取得
    weather_3pm = []
    for img in table.select('tr:nth-of-type(6) td img'):
        parent_td = img.find_parent('td')
        prev_sibling = parent_td.find_previous_sibling('td') if parent_td else None
        if prev_sibling and prev_sibling.get_text() != '-':
            weather_3pm.append(img['alt'])

    # 金曜日と土曜日の日付を抽出
    fridays_saturdays = [day for day, weekday in enumerate(calendar.monthcalendar(year, month), 1) if weekday in [4, 5] and day != 0]

    data = []
    for day, weather_15 in zip(days, weather_3pm):
        day_int = int(day)
        if day_int in fridays_saturdays:
            data.append({
                "year": str(year),
                "month": str(month),
                "day": day,
                "weather_3pm": weather_15
            })
    
    return data
def main():
    all_data = []
    
    for year in range(2018, 2023):  # 2018から2022まで
        for month in range(1, 13):  # 1月から12月まで
            url = base_url.format(year=year, month=str(month).zfill(2))  # 月を2桁に整形
            print(f"Fetching data for {year}-{month}...")
            monthly_data = extract_weather_data(url, year, month)
            all_data.extend(monthly_data)

    # データをJSONファイルとして保存
    with open("naha_weekend_weather_data.json", "w", encoding="utf-8") as f:
        json.dump(all_data, f, ensure_ascii=False, indent=4)

    print("Data fetching complete and saved to naha_weekend_weather_data.json!")

if __name__ == "__main__":
    main()