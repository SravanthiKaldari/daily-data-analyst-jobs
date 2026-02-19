import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
import os

EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")
EMAIL_TO   = os.getenv("EMAIL_TO")

# Search URLs (India + Remote focus)
# Search URLs (Multiple Platforms - India + Remote)
URLS = [

# Indeed
"https://www.indeed.co.in/jobs?q=entry+level+data+analyst&l=India",
"https://www.indeed.co.in/jobs?q=fresher+data+analyst&l=Remote",

# LinkedIn
"https://www.linkedin.com/jobs/search/?keywords=entry%20level%20data%20analyst&location=India",

# Naukri
"https://www.naukri.com/entry-level-data-analyst-jobs",

# Glassdoor
"https://www.glassdoor.co.in/Job/india-entry-level-data-analyst-jobs-SRCH_IL.0,5_IN115_KO6,30.htm",

# Startups (AngelList / Wellfound)
"https://wellfound.com/jobs?query=data%20analyst",


# AngelList (startups)
"https://wellfound.com/jobs?query=data%20analyst"
]


# keywords to ensure fresher-level roles
ENTRY_KEYWORDS = [
"entry",
"junior",
"fresher",
"trainee",
"associate",
"graduate",
"intern",
"internship",
"0-1",
"0 to 1",
"6 months",
"6month",
"six months"
]


def scrape():
    jobs = []
    headers = {"User-Agent": "Mozilla/5.0"}

    for url in URLS:
        try:
            r = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(r.text, "html.parser")

            for a in soup.find_all("a", href=True):
                title = a.get_text(strip=True)
                link = a["href"]

                if not title:
                    continue

                title_lower = title.lower()

                # filter only data analyst roles
                if "data analyst" not in title_lower:
                    continue

                # filter entry level keywords
                if not any(k in title_lower for k in ENTRY_KEYWORDS):
                    continue

                # remove unwanted links
                if "pagead" in link:
                    continue

                # fix relative links
                if link.startswith("/"):
                    link = url.split("/")[0] + "//" + url.split("/")[2] + link


                jobs.append((title, link))

        except Exception as e:
            print("Error:", e)

    # remove duplicates and limit to top 10
    unique_jobs = list(dict.fromkeys(jobs))[:10]
    return unique_jobs


def send_email(jobs):
    html = "<h2>Daily Entry-Level / Fresher Data Analyst Jobs</h2><ul>"

    if len(jobs) == 0:
        html += "<p>No fresh jobs found today.</p>"
    else:
        for title, link in jobs:
            html += f"<li><b>{title}</b><br><a href='{link}'>Apply Here</a></li><br>"

    html += "</ul>"

    msg = MIMEText(html, "html")
    msg["Subject"] = "Daily Fresher Data Analyst Jobs"
    msg["From"] = EMAIL_USER
    msg["To"] = EMAIL_TO

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(EMAIL_USER, EMAIL_PASS)
        server.sendmail(EMAIL_USER, EMAIL_TO, msg.as_string())


jobs = scrape()
send_email(jobs)


