import httplib2
import requests
import spacy
from bs4 import BeautifulSoup, SoupStrainer

http = httplib2.Http()

def get_page_links(url):
    links = []
    _, response = http.request(url)
    for link in BeautifulSoup(response, parse_only=SoupStrainer('p'), features="html.parser"):
        for a in link.find_all('a', href = True):
            if a['href'].startswith('/'):
                links.append("https://en.wikipedia.org" + a['href'])
    return links


def get_page_title(url):
    source = requests.get(url).text
    soup = BeautifulSoup(source, 'html.parser')
    return soup.find('title').text


def search(start_link, end_link, path = []):
    queue = [start_link]
    cur_link = start_link
    prev_link = start_link
    path_dict = {}
    while len(queue) >= 1:
        path.append(cur_link)
        queue.pop(0)
        for link in get_page_links(cur_link):
            if link not in path:
                if link in path_dict:
                    path_dict[link].append(cur_link)
                else:
                    path_dict[link] = [cur_link]
                if link == end_link:
                    path.append(link)
                    return path_dict
                queue.append(link)
        
        prev_link = cur_link
        cur_link = queue[0]
        path.pop()


def get_route(start_list, start, cur, corr_route, path_dict):
    corr_route.append(cur)
    print("cur: " + cur)
    if cur == start or start in start_list:
        corr_route.append(cur)
        return True
    for url in start_list:
        print("  " + url)
        if url in path_dict:
            if get_route(path_dict[url], start, url, corr_route, path_dict):
                return True 
    corr_route.pop()
    return False

def pprint(links):
    print("\nPath:")
    for link in links:
        print(f'\n{get_page_title(link)}\n({link})')


def get_input():
    start_url = input("Paste starting url:\n")
    end_url = input("Paste ending url:\n")
    assert start_url != end_url
    return start_url, end_url


def main():
    start_url, end_url = get_input()
    path = []
    path.append(start_url)
    path_dict = search(start_url, end_url)

    corr_route = []
    get_route(path_dict[end_url], start_url, end_url, corr_route, path_dict)

    pprint(corr_route)


if __name__ == '__main__':
    main()
    