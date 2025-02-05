import requests
import datetime
from bs4 import BeautifulSoup
import pandas as pd

# 검색 키워드와 페이지 수를 자동 설정
keyword = "데이터"
allpage = 1000

# 데이터를 저장할 리스트
data = []

# 페이지를 순회하며 데이터 수집
for page in range(1, int(allpage) + 1):
    url = f"https://www.saramin.co.kr/zf_user/search/recruit?search_area=main&search_done=y&search_optional_item=n&searchType=search&searchword={keyword}&recruitPage={page}&recruitSort=relation&recruitPageCount=40"
    
    soup = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    html = BeautifulSoup(soup.text, "html.parser")

    # 채용 정보 추출
    jobs = html.select("div.item_recruit")

    for job in jobs:
        try:
            today = datetime.datetime.now().strftime("%Y-%m-%d")
            title = job.select_one("a")["title"].strip().replace(",", "")
            company = job.select_one("div.area_corp > strong > a").text.strip()
            job_url = "https://www.saramin.co.kr" + job.select_one("a")["href"]
            deadline = job.select_one("span.date").text.strip()
            location = job.select("div.job_condition > span")[0].text.strip()
            experience = job.select("div.job_condition > span")[1].text.strip()
            requirement = job.select("div.job_condition > span")[2].text.strip()
            jobtype = job.select("div.job_condition > span")[3].text.strip()

            # 직무 분야(jobpart) 추가
            jobpart_elements = job.select("div.job_sector > b > a")
            jobpart = ", ".join([elem.text.strip() for elem in jobpart_elements])

            # 데이터를 리스트에 추가
            data.append(
                {
                    "today": today,
                    "title": title,
                    "company": company,
                    "url": job_url,
                    "deadline": deadline,
                    "location": location,
                    "experience": experience,
                    "requirement": requirement,
                    "jobtype": jobtype,
                    "jobpart": jobpart,
                }
            )
        except Exception:
            pass

# 데이터프레임 생성
df = pd.DataFrame(data)

# 오늘 날짜 기준 파일 이름 설정
date_str = datetime.datetime.now().strftime("%Y%m%d")
csv_filename = f"saramin_jobs_{date_str}.csv"

# 데이터 저장
df.to_csv(csv_filename, index=False)

print(f"데이터가 {csv_filename} 파일로 저장되었습니다.")
