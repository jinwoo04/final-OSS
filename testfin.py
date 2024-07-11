import requests
from bs4 import BeautifulSoup
from datetime import datetime

urls = [
    "https://www.kma.go.kr/wid/queryDFSRSS.jsp?zone=3017066000",
    "https://www.kma.go.kr/wid/queryDFSRSS.jsp?zone=1168066000",
    "https://www.kma.go.kr/wid/queryDFSRSS.jsp?zone=3114056000",
    "https://www.kma.go.kr/wid/queryDFSRSS.jsp?zone=2644053000",
    "https://www.kma.go.kr/wid/queryDFSRSS.jsp?zone=2920054000",
    "https://www.kma.go.kr/wid/queryDFSRSS.jsp?zone=5111035000"
]

headers = {
    'User-Agent': 'Mozilla/5.0',
    'Content-Type': 'text/html; charset=utf-8'
}

def fetch_weather_data(url,weather_list):
    req = requests.get(url, headers=headers)


    soup = BeautifulSoup(req.text, "lxml")

    category = soup.find("category").string.split()[0] #지역정보

    current_hour = datetime.now().hour
    closest_hour_data = None
    smallest_diff = float('inf')

    for item in soup.find_all("data"):
        hour = int(item.find("hour").string)
        diff = abs(current_hour - hour)
        if diff < smallest_diff:
            smallest_diff = diff
            closest_hour_data = item

    if closest_hour_data:
        hour = closest_hour_data.find("hour").string
        temp = closest_hour_data.find("temp").string
        reh = closest_hour_data.find("reh").string
        pop = closest_hour_data.find("pop").string 
        wfKor = closest_hour_data.find("wfkor").string
        r06 = closest_hour_data.find("r06").string
        weather_list.append((category,hour,temp,reh,pop,wfKor,r06))
    else:
        print("날씨정보가 없습니다.")

for url in urls:

    fetch_weather_data(url)
    print("\n")
