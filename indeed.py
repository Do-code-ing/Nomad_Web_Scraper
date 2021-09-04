import requests
from bs4 import BeautifulSoup

LIMIT = 50
URL = f"http://indeed.com/jobs?q=python&limit={LIMIT}"


def extract_indeed_pages():
    result = requests.get(URL)
    soup = BeautifulSoup(result.text, "html.parser")

    pagination = soup.find("div", {"class": "pagination"})
    links = pagination.find_all("a")
    pages = []

    for link in links[:-1]:
        pages.append(int(link.string))

    last_page = pages[-1]
    return last_page


def extract_indeed_jobs(last_pages):
    jobs = []
    for page in range(last_pages):
        result = requests.get(f"{URL}&start={page*LIMIT}")
        soup = BeautifulSoup(result.text, "html.parser")
        results = soup.find_all("a", {"class": "resultWithShelf"})
        for result in results:
            job_title = result.find("h2", {"class": "jobTitle"})
            title = job_title.find("span").string

            if title == "new":
                title = job_title.find_all("span")[1].string

            print(title)
    return jobs
