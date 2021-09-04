import requests

indeed_result = requests.get("http://indeed.com/jobs?q=python&limit=50")
