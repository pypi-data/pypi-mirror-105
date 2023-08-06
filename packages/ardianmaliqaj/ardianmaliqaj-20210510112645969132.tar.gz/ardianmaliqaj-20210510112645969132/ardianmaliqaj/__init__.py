from pprint import pprint
import requests
from bs4 import BeautifulSoup
from functools import lru_cache
from difflib import SequenceMatcher


@lru_cache(maxsize = 10000)
def similar(a, b):
	return SequenceMatcher(None, a, b).ratio()


@lru_cache(maxsize = 50)
def WebScrape(URL):
	r = requests.get(URL, headers = {'User-agent': 'Super Bot Power Level Over 9000'})
	result = BeautifulSoup(r.content, "html.parser").find("div", attrs = {"class":"BNeawe tAd8D AP7Wnd"})
	return result.text



def TextData(file):
	""" it turns a text tab and newline seperated data into
	a two dimensional list in a generator form. """
	header = None
	with open(file, "r") as file:
		for num, row in enumerate(file):
			row = row.strip().split("\t")
			yield row


def TransposeTextData(textdata):
	"""it transposes data that is received
	from TextData function. """
	return map(list, zip(*textdata))



def ToDict(textdata):
	""" it turns a textdata generator into a generator
	of dictionaries (in a key value format). """
	header = None
	for num, row in enumerate(textdata):
		if not num:
			header = row
			continue
		res = zip(header, row)
		yield dict(res)



