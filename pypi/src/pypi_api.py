import os
import tarfile

import requests
from bs4 import BeautifulSoup


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
    """Retrieve metadata for a given package name"""
    metadata_url = f"https://pypi.org/pypi/{package_name}/json"
    response = requests.get(metadata_url)
    if response.status_code == 200:
        return response.json()
    return {
        "msg": f"Failed to retrieve metadata for {package_name}: {response.reason}",
        "status": response.status_code,
    }


def extract_from_tarball(name: str, target_dir: str, tar_path: str):
    """Write tar contents to target directory"""
    if os.path.exists(tar_path) and os.path.getsize(tar_path) > 0:
        try:
            with tarfile.open(tar_path) as tar:
                tar.extractall(path=target_dir)
        except tarfile.ReadError:
            print(f"({name}) Failed to read {tar_path}.")
    else:
        print(f"({name}) {tar_path} does not exist or is empty.")


def download_tarball(url: str, name: str, target_dir: str):
    """Download from a given URL and extract to the target directory"""

    # create the target directory if it doesn't exist
    os.makedirs(target_dir, exist_ok=True)

    # download tar and save to target directory
    response = requests.get(url)
    if response.status_code == 200:
        tar_path = os.path.join(target_dir, f"{name}.tar.gz")
        with open(tar_path, "wb") as file:
            file.write(response.content)

        # extract from tar & clean up
        extract_from_tarball(name, target_dir, tar_path)
        os.remove(tar_path)
    else:
        print(f"({name}) Failed to download {url}")


def download_source_code(package_metadata: dict, target_dir: str) -> None:
    """Download the source code for a given package metadata"""
    name = package_metadata["info"]["name"]
    version = package_metadata["info"]["version"]

    # Find the source distribution URL (.tar.gz)
    for release in package_metadata["releases"][version]:
        if release["packagetype"] == "sdist":
            url = release["url"]
            break
    else:
        print(f"({name}) No source distribution found for {name}-{version}")
        return

    download_tarball(url, name, target_dir)
