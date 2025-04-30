import re
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urldefrag, parse_qs, urljoin
from helpers import is_too_similar, tokenize, computeWordFrequencies, stop_words
from collections import Counter, defaultdict

unique_pages = set()
global_word_freq = Counter()
subdomain_page_sets = defaultdict(set)
longest_page = {
    "url":    None,
    "length": 0
}
pages_since_report = 0

already_visited = set()
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
    
    # try to parse with bs4, if can't assume bad site and return []
    try:
        parsed_html = BeautifulSoup(resp.raw_response.content, "lxml")

        # exclude text within blacklisted tags, only want raw text
        for blacklist_tag in parsed_html(blacklisted_tags):
            blacklist_tag.decompose()

        # process text from the site
        text = parsed_html.get_text(separator=" ", strip=True)
        tokens = tokenize(text)
        token_dict = computeWordFrequencies(tokens)

        # skip pages with 200 status but no information
        if len(token_dict) <= 20 or len(tokens) <= 50:
            return []
        
        # avoid sites with high link to token density to avoid gallery like sites
        link_count = len(parsed_html.find_all("a", href=True))
        if link_count / max(len(tokens), 1) > 0.3:
            return []
        
        # if the current text is similar to 3+ other fingerprints, dont add urls
        if is_too_similar(url, tokens) >= 3:
            return []
        
        # only add text to report with token count to unique token ratio (informational value) 0.2 or higher
        informational_value = len(token_dict) / len(tokens)
        if informational_value >= 0.2:
            clean_url, _ = urldefrag(resp.url)
            unique_pages.add(clean_url)

            page_word_count = sum(token_dict.values())
            if page_word_count > longest_page["length"]:
                longest_page["length"] = page_word_count
                longest_page["url"]    = clean_url

            global_word_freq.update(token_dict)

            domain = urlparse(resp.url).netloc.lower()
            if domain.endswith("uci.edu"):
                subdomain_page_sets[domain].add(clean_url)

            global pages_since_report
            pages_since_report += 1
            print(pages_since_report)
            if pages_since_report >= 50:
                write_report()
                pages_since_report = 0

        all_a_tags = parsed_html.find_all("a", href=True)
        list_of_next_urls = []

        # url normalization
        for link in all_a_tags:
            href_url = link["href"]
            full_url = urljoin(resp.url, href_url)
            clean_url, _ = urldefrag(full_url)
            list_of_next_urls.append(clean_url)

        # remove potential duplicates to avoid unnecessary clutter
        list_of_next_urls = list(set(list_of_next_urls))
        return list_of_next_urls
    except Exception:
        return []

def write_report():
    lines = []
    lines.append(f"Total unique pages: {len(unique_pages)}\n")
    lines.append(f"Longest page: {longest_page['url']} "
                 f"({longest_page['length']} words)\n\n")
    lines.append("Top 50 most common words:\n")
    for word, freq in global_word_freq.most_common(50):
        lines.append(f"{word}: {freq}\n")
    lines.append("\nSubdomain counts:\n")
    for subd in sorted(subdomain_page_sets):
        lines.append(f"{subd}, {len(subdomain_page_sets[subd])}\n")

    with open("crawl_report.txt", "w") as report:
        report.writelines(lines)

def is_valid(url):
    # Decide whether to crawl this url or not. 
    # If you decide to crawl it, return True; otherwise return False.
    # There are already some conditions that return False.
    try:
        if url in already_visited:
            return False
        
        already_visited.add(url)
        parsed = urlparse(url)

        domain = parsed.netloc.lower()
        path = parsed.path or '/'

        if domain == "grape.ics.uci.edu":
            return False

        valid_domain = (
        domain.endswith("ics.uci.edu")
        or domain.endswith("cs.uci.edu")
        or domain.endswith("informatics.uci.edu")
        or domain.endswith("stat.uci.edu")
        or (domain == "today.uci.edu" and path.startswith("/department/information_computer_sciences/"))
        )

        if not valid_domain:
            return False

        if parsed.scheme not in set(["http", "https"]):
            return False
        
        # do not include urls with filter query parameters to avoid infinite trap
        query_params = parse_qs(parsed.query)
        if any("filter" in query.lower() for query in query_params):
            return False
        
        # dont allow urls with more than 2 query parameters, possible trap
        if parsed.query and parsed.query.count("&") > 2:
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
        
        return True

    except TypeError:
        print ("TypeError for ", parsed)
        raise