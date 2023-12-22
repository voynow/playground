import requests
from bs4 import BeautifulSoup


def get_packages(response):
    """
    Find all <a> tags, which contain the package names and links
    Extract package names from the links
    """

    soup = BeautifulSoup(response.text, "html.parser")
    links = soup.find_all("a")
    packages = [link.get_text() for link in links]

    return packages


def get_all_packages():
    """"""
    response = requests.get("https://pypi.org/simple/")
    return get_packages(response)
