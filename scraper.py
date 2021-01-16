import pandas as pd
import mechanicalsoup
browser = mechanicalsoup.StatefulBrowser()

# USING THE ETL
def extract(page):
#     headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36'}
    url = f'https://www.indeed.co.uk/jobs?q=data+scientist&l=London,+Greater+London&start={page}'
    browser.open(url)
    soup = browser.get_current_page()
    return soup


def transform(soup):
    divs = soup.find_all('div', class_ = 'jobsearch-SerpJobCard')
    for item in divs:
        title = item.find('a').text.strip()
        company = item.find('span', class_='company').text.strip()
#         rating = item.find('span', {'id': 'text'}).text.strip()
        location = item.find('span', class_ = 'location').text.strip()
        try:
            salary = item.find('span', 'salaryText').text.strip()
        except:
            salary = ''
        summary = item.find('div', {'class': 'summary'}).text.strip().replace('\n', '')
        
        jobs = {
            'title':title,
            'company':company,
            'location': location,
            'salary':salary,
            'summary': summary
        }
        
        joblist.append(jobs)
    return

joblist = []

# run thru 10 pages getting 10 job per page
for i in range(0, 100, 10):
    print(f'Getting jobs post {i}')
    soup = extract(i)
    transform(soup)

df = pd.DataFrame(joblist)
df.head()

df.to_csv('jobs.csv')