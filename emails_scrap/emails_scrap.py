from bs4 import BeautifulSoup as bs
import requests
from urllib.parse import urlsplit
from collections import deque
import re
import csv 

def scrap(data): 
    #urls для обхода
    new_urls = deque([data])
     
    #urls, которые уже обошли
    processed_urls = set()
     
    #emails, которые уже собраны
    emails = set()
     
    while len(new_urls):

        url = new_urls.popleft()
        processed_urls.add(url)
     
        #коснтруктор urls
        parts = urlsplit(url)
        base_url = "{0.scheme}://{0.netloc}".format(parts)
        if parts.scheme !='mailto' and parts.scheme !='#':
            path = url[:url.rfind('/')+1] if '/' in parts.path else url
        else:
            continue
     
        print("Processing %s" % url)
        try:
            response = requests.get(url)
        except (requests.exceptions.MissingSchema, requests.exceptions.ConnectionError, requests.exceptions.InvalidURL):
            continue
     
        #извлечение всех найденых emails
        new_emails = set(re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", response.text, re.I))
        emails.update(new_emails)
     
        soup = bs(response.text, 'lxml')
     
        for anchor in soup.find_all("a"):
            link = anchor.attrs["href"] if "href" in anchor.attrs and anchor.attrs["href"].find("mailto") ==-1 and anchor.attrs["href"].find("tel") ==-1 and anchor.attrs["href"].find("#") ==-1  else ''

            if link.startswith('/'):
                link = base_url + link
            elif not link.startswith('http'):
                link = path + link
            if '.pdf' in link or '.png' in link or '.jpg' in link:
                continue
            else:        
                if not link in new_urls and not link in processed_urls and not link.find(data) == -1:
                    new_urls.append(link)

    return emails if len(emails) > 0 else 'Page not found or Error' 


def write_csv(data):
	with open('emails.csv', 'a') as f:
		writer = csv.writer(f)

		writer.writerow( (data['url'],
						  data['email']) )

def read_file():
	try:
		with open('urls_list.txt', 'r+', encoding = 'UTF-8') as urls: #чтение из файла
			array = [row.strip() for row in urls]
		return array		
		
	except IOError as er:
		print(u'Can\'t open the "{0}" file'.format(er.filename))


def main():
    for url in read_file():
        data = {'url': url,
                'email': scrap(url)}        
        write_csv(data)


if __name__ == '__main__':
    main()



	

#input("Press Enter")
