from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq
import progressbar, pickle, json

def get_soup(url):
    page = uReq(url)
    html = page.read()
    page_soup = soup(html, 'html.parser')
    return page_soup

def get_reference_years(imdb_id):
    page_soup = get_soup('https://www.imdb.com/title/' + imdb_id + '/movieconnections/')
    title = page_soup.find('title').text.split(' - Connections - ')[0]
    year = int(page_soup.find('title').text.split(') - Connections - ')[0].split(' (')[-1])
    content = page_soup.find('div', {'id': 'connections_content'}).find('div', {'class': 'list'})
    children = content.findChildren(recursive=False)

    reference_years = []
    references = []
    finding = False
    for child in children:
        if child.name == 'h4':
            if 'References' in child.text:
                finding = True
            elif finding:
                break
        elif finding:
            if child.text:
                try:
                    reference_years.append(int(child.text.split('\xa0(')[1].split(')')[0]))
                    references.append(child.text)
                except:
                    print(imdb_id)
    return year, title, reference_years, references

def get_titles(year):
    url = 'https://www.imdb.com/search/title?title_type=feature&release_date='+str(year)+'-01-01,'+str(year)+'-12-31'
    page_soup = get_soup(url)
    headers = page_soup.findAll('h3', {'class': 'lister-item-header'})
    ids = [h3.find('a').attrs['href'].split("/")[2] for h3 in headers]
    url = 'https://www.imdb.com/search/title?title_type=feature&release_date='+str(year)+'-01-01,'+str(year)+'-12-31&start=51'
    page_soup = get_soup(url)
    headers = page_soup.findAll('h3', {'class': 'lister-item-header'})
    ids += [h3.find('a').attrs['href'].split("/")[2] for h3 in headers]
    url = 'https://www.imdb.com/search/title?title_type=feature&release_date='+str(year)+'-01-01,'+str(year)+'-12-31&start=101'
    page_soup = get_soup(url)
    headers = page_soup.findAll('h3', {'class': 'lister-item-header'})
    ids += [h3.find('a').attrs['href'].split("/")[2] for h3 in headers]
    url = 'https://www.imdb.com/search/title?title_type=feature&release_date='+str(year)+'-01-01,'+str(year)+'-12-31&start=151'
    page_soup = get_soup(url)
    headers = page_soup.findAll('h3', {'class': 'lister-item-header'})
    ids += [h3.find('a').attrs['href'].split("/")[2] for h3 in headers]
    return ids

imdb_ids = []
for year in progressbar.progressbar(range(1900, 2019)):
    imdb_ids += get_titles(year)

data = {}
for imdb_id in progressbar.progressbar(imdb_ids):
    year, title, reference_years, references = get_reference_years(imdb_id)
    if year not in list(data.keys()):
        data[year] = {}
    for i in range(len(reference_years)):
        ref_year = reference_years[i]
        reference = references[i]
        if ref_year not in list(data[year].keys()):
            data[year][ref_year] = [0, {}]
        data[year][ref_year][0] += 1
        if title not in list(data[year][ref_year][1].keys()):
            data[year][ref_year][1][title] = []
        data[year][ref_year][1][title].append(reference)

pickle.dump(data, open('data.p', 'wb'))
f = open('src/json/data.json', 'w')
f.write(json.dumps(data))
f.close()
