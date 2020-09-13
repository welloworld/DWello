import requests
import re
from bs4 import BeautifulSoup
from article import Article

NUM_OF_ISSUES = 100 #Maybe will be dynamic in the future.
HEBREW_WRITTEN_BY_PREFIX = ['- נכתב ע"י','-\xa0נכתב ע"י', '-\xa0מאת', '- מאת']
HEBREW_RELEASE_DATE_PREFIX = 'תאריך יציאה: '
OUTPUT_FILE_GENERAL = 'DWello_general.txt'
OUTPUT_FILE_AUTHORS = 'DWello_authors.txt'

URL = 'https://www.digitalwhisper.co.il/issue'

def get_parts_list(url_path):
	return list(filter(lambda part: part != '', url_path.split('/')))

def relative_to_absolute(rel, curr):
	"""
	This function translates a relative path from specific place on the site - to be absolute
	NOTE: this function assumes that the `..` can be only in the beginning of the relative path
	"""
	if '..' not in rel:
		return rel

	relParts = get_parts_list(rel)
	currParts = get_parts_list(curr)
	urlPrefix = '//'.join(currParts[:2]) # http://www.digitalwhisper.co.il/
	currParts = currParts[:2] # removes `http://www.digitalwhisper.co.il`

	for part in relParts:
		if part == '..' and len(currParts):
			currParts.pop()

	relParts = list(filter(lambda part: part != '..' and part != 'http:' and part != 'www.digitalwhisper.co.il', relParts))

	relStr =  '/' + '/'.join(relParts)
	currStr = '/' + '/'.join(currParts)

	currStr = '' if len(currStr) == 1 else currStr
	
	return urlPrefix + currStr + relStr

def parse_article(tr, date, issueNum):
	"""
	This function returns the needed attributes of an article by the given html `tr` tag.
	"""

	articleInfo, authorInfo = tr.find_all('td')

	link = relative_to_absolute(articleInfo.a['href'], URL)
	name = articleInfo.a.text
	author = authorInfo.text.strip()
	for i in HEBREW_WRITTEN_BY_PREFIX: author = author.replace(i,'')
	author = author.strip()

	return Article(name, author, link, date, issueNum) #date meanwhile

def find_date(soup):
	"""
	This function returns the date from an issue
	"""
	for div in soup.find_all('div'):
		try:
			found = re.search(HEBREW_RELEASE_DATE_PREFIX + '[0-9]{1,2}\/[0-9]{1,2}\/[0-9]{1,2}', div.text).group()

			if found:
				return found.replace(HEBREW_RELEASE_DATE_PREFIX,'').strip()
		except:
			pass

	return '~can not find date~'		

def is_tr_ok(tr):
	"""
	This function checks whether html `tr` tag is ok and defined well
	"""
	return (tr.td.text and tr.td.text != ' ' and tr.td.text != chr(160)) #Unicode character NO-BREAK SPACE


def get_all_articles():
	"""
	This function returns data on the articles from the site by the site's issues.
	"""
	articles = []
	print(f'[*] Get data from {NUM_OF_ISSUES-1} issues [*]')
	print()
	
	for issueNum in range(1,NUM_OF_ISSUES):
		print(f'# [{issueNum}] #')
		res = requests.get(URL + str(issueNum)).text
		soup = BeautifulSoup(res, 'html.parser')
		content_table = soup.find_all('table')
		assert(len(content_table) == 1) # We expects only one table in an article page

		date = find_date(soup)
		for article in content_table[0].tbody.find_all('tr')[1:]: # The first row is "name of article" and "name of author"
			if is_tr_ok(article):
				articles.append(parse_article(article, date, issueNum))
	return articles

def main():
	articles = get_all_articles()
	print()
	with open(OUTPUT_FILE_GENERAL, 'w', encoding="utf-8") as outputFile:
		outputFile.write('\n'.join(str(x) for x in articles)) # for saving all the data on articles
		print(f'[*] General data saved to "{OUTPUT_FILE_GENERAL}" [*]')

	with open(OUTPUT_FILE_AUTHORS, 'w', encoding="utf-8") as outputFile:
		outputFile.write('\n'.join(x.authorName for x in articles)) #for saving all the data on article authors
		print(f'[*] Authors data saved to "{OUTPUT_FILE_AUTHORS}" [*]')


if __name__ == '__main__':
	main()
