'''
Created by https://github.com/asciidea/wikidea
V. 1.0.0
Author: Alisson
'''

from bs4 import BeautifulSoup as bs
import requests
import argparse
import json

parser = argparse.ArgumentParser()

helps = [
	"--wiki <article name> return wikipedia article text.",
	"--index <paragraph index> set wikipedia article page paragraph.",
	"--lang <wikipedia language en | pt | es | ...> set wikipedia server region.",
	"--find <article keyword> search article names"
]

def create_parse(_parser):
	_parser.add_argument("--wiki", dest = 'wiki_l', required=False, default='', help=helps[0])
	_parser.add_argument("--index", dest = 'wiki_p', required=False, type = int, default = -1, help=helps[1])
	_parser.add_argument("--lang", dest = 'wiki_e', required=False, type=str, default='en', help=helps[2])
	_parser.add_argument("--find", dest = 'wiki_f', required=False, type=str, help=helps[3])
	pass
create_parse(parser)
args = parser.parse_args()

def make_search(r, index, l):
	u = requests.get("https://{}.wikipedia.org/wiki/{}".format(l, r)).text
	v = bs(u, "html.parser")
	w = v.find("div", {
		"class": "mw-parser-output"
		})

	if w:
		x = bs(w.decode(), "html.parser").find_all("p")
	
		if not index < 0:
			if index < len(x):
				x = x[index]
			else:
				print("$ index > page paragraphs! changed index to 0")
				x = x[0]
			print(x.text)
		else:
			for i in range(len(x)):
				print(x[i].text)
	else:
		print("this article not exists")
	
def search_article(lang, keyword):
	r = requests.get("https://{}.wikipedia.org/w/api.php?action=opensearch&search={}".format(lang, keyword)).text
	search_values = json.loads(r)[1]
	
	for i in range(len(search_values)):
		print(i, " {}".format(search_values[i]))
	
	_max = len(search_values)

	if len(search_values) > 0:
		while True:
			x = input("Type search index number: ")
			if x.isnumeric():
				if int(x) < _max and int(x) > -1:
					print("++in your marks...")
					make_search(search_values[int(x)], args.wiki_p, args.wiki_e)
					break
	else:
		print("error 404! ooooohhh, sorry!")
	pass

if len(args.wiki_l) > 0:
	make_search(args.wiki_l, args.wiki_p, args.wiki_e)
elif args.wiki_f:
	search_article(args.wiki_e, args.wiki_f)
else:
	print("$ --wiki needs a article name")