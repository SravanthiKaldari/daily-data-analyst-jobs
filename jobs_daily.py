import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
import os

EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")
EMAIL_TO   = os.getenv("EMAIL_TO")

URLS = [
"https://www.linkedin.com/jobs/search/?keywords=entry%20level%20data%20analyst",
"https://www.indeed.com/jobs?q=entry+level+data+analyst",
"https://angel.co/jobs?keywords=data%20analyst"
]

def scrape():
    jobs=[]
    headers={"User-Agent":"Mozilla/5.0"}

    for url in URLS:
        r=requests.get(url,headers=headers,timeout=10)
        soup=BeautifulSoup(r.text,"html.parser")

        for link in soup.find_all("a",href=True):
            title=link.text.strip()
            href=link["href"]

            if "data analyst" in title.lower() and len(title)>8:
                jobs.append((title,href))

    return list(dict.fromkeys(jobs))[:20]

def send_email(jobs):
    html="<h2>Daily Entry Level Data Analyst Jobs</h2><ul>"
    for title,link in jobs:
        html+=f"<li>{title} - <a href='{link}'>Apply</a></li>"
    html+="</ul>"

    msg=MIMEText(html,"html")
    msg["Subject"]="Daily Data Analyst Jobs"
    msg["From"]=EMAIL_USER
    msg["To"]=EMAIL_TO

    with smtplib.SMTP_SSL("smtp.gmail.com",465) as server:
        server.login(EMAIL_USER,EMAIL_PASS)
        server.sendmail(EMAIL_USER,EMAIL_TO,msg.as_string())

jobs=scrape()
send_email(jobs)
