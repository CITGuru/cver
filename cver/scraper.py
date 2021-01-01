import requests
from bs4 import BeautifulSoup

SEARCH_URL = "https://cve.mitre.org/cgi-bin/cvekey.cgi?keyword="
CVE_URL = "https://cve.mitre.org/cgi-bin/cvename.cgi?name="


def get_html(url):
    request = requests.get(url)
    if request.status_code == 200:
        return request.content
    else:
        raise Exception("Bad request")


def extract_rows(row):

    _row = {}
    name = row.select_one("td a")
    description = row.select_one("td:nth-child(2)")
    if all([name, description]):
        _row["name"] = name.text
        _row["url"] = name.get("href")
        _row["description"] = description.text

        return _row


def search(s):
    url = f"{SEARCH_URL}{s}"
    html = get_html(url)
    soup = BeautifulSoup(html, "lxml")
    result_rows = soup.select("#TableWithRules table tr")

    results = map(extract_rows, result_rows)
    results = list(results)

    return results

def lookup_cve(name):
    url = f"{CVE_URL}{name}"
    html = get_html(url)
    soup = BeautifulSoup(html, "lxml")
    result_rows = soup.select("#GeneratedTable table tr")

    subtitle = ""
    description = ""

    raw_results = {}

    for row in result_rows:
        head = row.select_one("th")
        if head:
            subtitle = head.text
        else:
            body = row.select_one("td")
            description = body.text.strip().strip("\n")
            raw_results[subtitle.lower()] = description

    return raw_results
