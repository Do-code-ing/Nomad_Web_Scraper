import requests
from bs4 import BeautifulSoup

LIMIT = 50
URL = f"http://indeed.com/jobs?q=python&limit={LIMIT}"


def get_last_page():
    result = requests.get(URL)
    soup = BeautifulSoup(result.text, "html.parser")
    pagination = soup.find("div", {"class": "pagination"})
    links = pagination.find_all("a")
    pages = []
    for link in links[:-1]:
        pages.append(int(link.string))

    last_page = pages[-1]
    return last_page


def extract_job(soup):
    job_title = soup.find("h2", {"class": "jobTitle"})
    title = job_title.find("span").string
    if title == "new":
        title = job_title.find_all("span")[1].string
    company = soup.find("span", {"class": "companyName"}).string
    location = soup.find("div", {"class": "companyLocation"}).text
    job_id = soup["data-jk"]

    return {
        "title": title,
        "company": company,
        "location": location,
        "apply_link": f"https://www.indeed.com/viewjob?jk={job_id}"}


def extract_jobs(last_pages):
    jobs = []
    for page in range(last_pages):
        print(f"Scrapping Indeed page {page}")
        result = requests.get(f"{URL}&start={page*LIMIT}")
        soup = BeautifulSoup(result.text, "html.parser")
        results = soup.find_all("a", {"class": "resultWithShelf"})
        for result in results:
            job = extract_job(result)
            jobs.append(job)

    return jobs


def get_jobs():
    last_page = get_last_page()
    jobs = extract_jobs(last_page)
    return jobs
