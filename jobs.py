import requests # make a request to retrieve URL page
from bs4 import BeautifulSoup # HTML parser
import pandas as pd
from datetime import datetime

base_url = "https://realpython.github.io/fake-jobs/"
header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36"}

print("Connecting..")
response_page = requests.get(base_url, headers=header)

if response_page.status_code == 200:
    print("Connected")
else:
    print("Connection not Successful")

print(response_page.text)


parsed_page = BeautifulSoup(response_page.text, 'html.parser')

job_listing = parsed_page.find_all('div', class_="column is-half")

all_job_listings = []
for listing in job_listing:
    job_name = listing.find('h2').text.strip()
    company_name = listing.find('h3').text.strip()
    location = listing.find('p', class_='location').text.strip().split()
    location = " ".join(location).split(' - ')
    location_city = location[0].split(',')[0]
    location_state = location[0].split(',')[1].strip()
    date_posted_str = listing.find('time')['datetime']
    date_posted = datetime.strptime(date_posted_str, '%Y-%m-%d')
    day_of_week = date_posted.strftime('%A')
    day_month = date_posted.strftime('%d' '%B')
    year = date_posted.year

    all_job_listings.append({
        'Job Title': job_name,
        'Company Name': company_name,
        'City': location_city.strip(),
        'State': location_state,
        'Date Posted': date_posted,
        'Day of Week, Day and Month': day_of_week + ', ' + day_month,
        'Year': year
    })
   
jobs_df = pd.DataFrame(all_job_listings)
pd.set_option("display.max_columns", None) 

print(jobs_df)

