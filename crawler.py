import requests
from bs4 import BeautifulSoup
import json
import jdatetime

url = 'https://www.time.ir/'
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

day_list_div = soup.find('div', class_='dayList')
date_list_div = soup.find('div', class_='today-shamsi')
today_date = date_list_div.find('span', class_="show numeral").contents[0].split("/")

dates_info = {}
monthDay = 0
weekDay = 0
for day_div in day_list_div.find_all('div', recursive=False):
    is_today = False
    classes = day_div.get('class', [])
    if weekDay == 7:
        weekDay = 0
        
    weekDay += 1
    if 'spacer' in classes or 'disabled' in classes:
        continue
    elif 'today' in classes:
        monthDay += 1
        is_today = True
    else:
        monthDay += 1
    
    dates_info[monthDay] = {
        "weekDay": weekDay, 
        "is_holiday": False, 
        "is_today": is_today, 
        "year": int(today_date[0]), 
        "month": int(today_date[1]), 
        "day": monthDay
    }
    
    if day_div.find('div', class_='holiday') is not None:
        dates_info[monthDay]["is_holiday"] = True

for day, info in dates_info.items():
    shamsi_date = jdatetime.date(info["year"], info["month"], info["day"])
    miladi_date = shamsi_date.togregorian()
    dates_info[day]["miladi_date"] = str(miladi_date)

json_object = json.dumps(dates_info, indent=4) 
print(json_object)
