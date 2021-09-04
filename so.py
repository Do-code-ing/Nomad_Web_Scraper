import requests
from bs4 import BeautifulSoup

URL = f"https://stackoverflow.com/jobs?q=python"


def get_last_page():
    result = requests.get(URL)
    soup = BeautifulSoup(result.text, "html.parser")
    pages = soup.find("div", {"class": "s-pagination"}).find_all("a")
    last_page = pages[-2].get_text(strip=True)
    return int(last_page)


def extract_job(soup):
    title = soup.find("h2").find("a")["title"]
    company_row = soup.find("h3").find_all("span")
    company = company_row[0].get_text(strip=True)
    location = company_row[1].get_text(strip=True)
    job_id = soup["data-jobid"]

    return {
        "title": title,
        "company": company,
        "location": location,
        "apply_link": f"https://stackoverflow.com/jobs/{job_id}"}


def extract_jobs(last_page):
    jobs = []
    for page in range(1, last_page+1):
        print(f"Scrapping SO page {page}")
        result = requests.get(f"{URL}&pg={page}")
        soup = BeautifulSoup(result.text, "html.parser")
        results = soup.find_all("div", {"class": "-job"})
        for result in results:
            job = extract_job(result)
            jobs.append(job)

    return jobs


def get_jobs():
    last_page = get_last_page()
    jobs = extract_jobs(last_page)
    return jobs
