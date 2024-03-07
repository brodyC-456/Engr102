import requests
import time
from bs4 import BeautifulSoup as bs
from collections import Counter

class Quote:
    def __init__(self, text, author, tags):
        self.text = text
        self.author = author
        self.tags = tags

def main():
    url = "https://quotes.toscrape.com"
    r = requests.get(url)
    soup = bs(r.content, "html.parser")

    #scrape_quotes(soup)

    quotes = []
    while True:
        time.sleep(1)
        relative_url = get_next_url(soup)
        if relative_url is None:
            break
        next_page = url + relative_url

        r = requests.get(next_page)
        soup = bs(r.content, "html.parser")
        quotes.extend(scrape_quotes(soup))

        get_shortest_and_longest(quotes)
        
    print(top_ten_tags(quotes))
    print(multiple_authors(quotes))

    return

def multiple_authors(quotes):
    author_list = []
    for quote in quotes:
        author_list.append(quote.author)
    author_list.sort()
    author_count = Counter(author_list)
    multiple_author_list = []
    for author, author_count in author_count.items():
        if author_count > 1:
            multiple_author_list.append((author, author_count))
    
    return multiple_author_list


def top_ten_tags(quotes):

    tags = []
    for quote in quotes:
        tags.extend(quote.tags)
    tags.sort()
    count = Counter(tags)
    top_ten = count.most_common(10)
    return (top_ten)
    

    return


def get_next_url(soup: bs):
    
    list_item = soup.find("li", {"class": "next"})
    if list_item is None:
        return None
    anchor = list_item.find("a")
    url = anchor["href"]

    return url

def get_shortest_and_longest(quotes):

    longest = 0
    shortest = 100000
    longest_quote = ""
    shortest_quote = ""
    for quote in quotes:
        if len(quote.text) > longest:
            longest = len(quote.text)
            longest_quote = quote.text

        if len(quote.text) < shortest:
            shortest = len(quote.text)
            shortest_quote = quote.text

    return



def scrape_quotes(soup: bs):
    quotes = soup.find_all("div", {"class": "quote"})
    quotes_list = []
    for quote in quotes:
        text = quote.find("span", {"class": "text"}).get_text(strip = True)
        print(text)
        author = quote.find("small", {"class": "author"}).get_text(strip = True)
        print(author)
        tags = quote.find_all("a", {"class": "tag"})
        tags_text = []
        for tag in tags:
            tags_text.append(tag.get_text(strip = True))
        print(tags_text)
        print("----------------------------")
       
        quotes_list.append(Quote(text, author, tags_text))

    return quotes_list




if __name__ == "__main__":
    main()
