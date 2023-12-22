import os

import requests
from bs4 import BeautifulSoup

LICENSE_WHITELIST = [
    "Apache-2.0",
    "Apache Software License",
    "MIT",
    "BSD",
    "ISC",
    "LGPL",
    "MPL-2.0",
    "Unlicense",
]


def get_packages():
    """
    Retrieve a list of all packages on PyPI, Find all <a> tags which contain
    the package names and links, extract package names from the links
    """
    response = requests.get("https://pypi.org/simple/")

    soup = BeautifulSoup(response.text, "html.parser")
    links = soup.find_all("a")
    packages = [link.get_text() for link in links]

    return packages


def get_package_metadata(package_name: str) -> dict:
    """
    Retrieve metadata for a given package name
    By default we assume no license whitelist
    """
    metadata_url = f"https://pypi.org/pypi/{package_name}/json"
    response = requests.get(metadata_url)
    if response.status_code == 200:
        return response.json()
    return {"msg": f"Failed to retrieve {package_name}"}


def download_package_zip(name: str, url: str, download_path: str = "downloads") -> str:
    """Download package zip from a given URL"""
    response = requests.get(url, stream=True)

    if response.status_code == 200:
        path = f"{download_path}/{name}/downloaded_package.zip"

        # create directory if it doesn't exist
        os.makedirs(os.path.dirname(path), exist_ok=True)

        # download file
        with open(path, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)

        return "Package downloaded successfully."
    return f"Failed to download package. Status code: {response.status_code}"
