import re
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urldefrag, urljoin

already_visited = set()
current_prefix_depth = {}
blacklisted_tags = {
    "script",
    "style",
    "head",
    "meta",
    "title",
    "link",
    "noscript",
    "nav",
    "header",
    "footer",
    "aside",
    "form",
    "input",
    "button",
    "select",
    "textarea",
    "option",
    "svg",
    "canvas",
    "iframe",
    "object",
    "embed"
}

def scraper(url, resp):
    links = extract_next_links(url, resp)
    # for link in links:
    #     print(f"{link}, {is_valid(link)}")
    return [link for link in links if is_valid(link)]

def extract_next_links(url, resp):
    # Implementation required.
    # url: the URL that was used to get the page
    # resp.url: the actual url of the page
    # resp.status: the status code returned by the server. 200 is OK, you got the page. Other numbers mean that there was some kind of problem.
    # resp.error: when status is not 200, you can check the error here, if needed.
    # resp.raw_response: this is where the page actually is. More specifically, the raw_response has two parts:
    #         resp.raw_response.url: the url, again
    #         resp.raw_response.content: the content of the page!
    # Return a list with the hyperlinks (as strings) scrapped from resp.raw_response.content

    if (not (200 <= resp.status < 300)) or (not resp.raw_response.content):
        return []
    
    # parse the html with beautiful soup into bs4 object
    parsed_html = BeautifulSoup(resp.raw_response.content, "lxml")

    # exclude text within blacklisted tags, only want raw text
    for blacklist_tag in parsed_html(blacklisted_tags):
        blacklist_tag.decompose()

    text = parsed_html.get_text(separator=" ", strip=True)
    with open("test_text.txt", "a", encoding="utf-8") as f:
        # a clear separator with the URL
        f.write("\n" + "="*80 + "\n")
        f.write(f"URL: {url}\n")
        f.write("="*80 + "\n\n")
        # the page’s text
        f.write(text + "\n\n")

    # from bs4 object find all a tags that has href in it
    all_a_tags = parsed_html.find_all("a", href=True)
    list_of_next_urls = []

    # no need for url validation checking, that is done in scraper.py
    # urljoin ensures the whole url is returned since urls within a href's can vary
    # urldefrag removes the fragment at the end of the url if it exists
    for link in all_a_tags:
        href_url = link["href"]
        full_url = urljoin(resp.url, href_url)
        clean_url, _ = urldefrag(full_url)
        list_of_next_urls.append(clean_url)
    
    # 
    
    return list_of_next_urls


def is_valid(url):
    # Decide whether to crawl this url or not. 
    # If you decide to crawl it, return True; otherwise return False.
    # There are already some conditions that return False.
    try:
        parsed = urlparse(url)

        if parsed in already_visited:
            return False

        domain = parsed.netloc.lower()
        path = parsed.path or '/'

        valid_domain = (
        domain.endswith(".ics.uci.edu")
        or domain.endswith(".cs.uci.edu")
        or domain.endswith(".informatics.uci.edu")
        or domain.endswith(".stat.uci.edu")
        or (domain == "today.uci.edu"
            and path.startswith("/department/information_computer_sciences/"))
        )

        if not valid_domain:
            return False

        if parsed.scheme not in set(["http", "https"]):
            return False
        
        # should be the last check
        if (re.match(
            r".*\.(css|js|bmp|gif|jpe?g|ico"
            + r"|png|tiff?|mid|mp2|mp3|mp4"
            + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
            + r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names"
            + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
            + r"|epub|dll|cnf|tgz|sha1"
            + r"|thmx|mso|arff|rtf|jar|csv"
            + r"|rm|smil|wmv|swf|wma|zip|rar|gz)$", parsed.path.lower())):
            return False
        already_visited.add(parsed)
        return True

    except TypeError:
        print ("TypeError for ", parsed)
        raise
