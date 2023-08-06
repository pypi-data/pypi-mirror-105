#!/usr/bin/env python3
"""ALPHA VIDEO setup script."""
from datetime import datetime as dt

from setuptools import find_packages, setup

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

PROJECT_NAME = "Alpha Video"
PROJECT_PACKAGE_NAME = "alpha-video"
PROJECT_LICENSE = "Apache License 2.0"
PROJECT_AUTHOR = "Unofficial-skills"
PROJECT_COPYRIGHT = f" 2021-{dt.now().year}, {PROJECT_AUTHOR}"
PROJECT_URL = "https://alpha-video.andrewstech.me/"
PROJECT_EMAIL = "hello@andrewstech.me"

PROJECT_GITHUB_USERNAME = "unofficial-skills"
PROJECT_GITHUB_REPOSITORY = "alpha-video"

PYPI_URL = f"https://pypi.python.org/pypi/{PROJECT_PACKAGE_NAME}"
GITHUB_PATH = f"{PROJECT_GITHUB_USERNAME}/{PROJECT_GITHUB_REPOSITORY}"
GITHUB_URL = f"https://github.com/{GITHUB_PATH}"

PROJECT_URLS = {
    "Bug Reports": f"{GITHUB_URL}/issues",
    "Dev Docs": "https://alpha-video.andrewstech.me/",
    "Discord": "https://discord.gg/WAu8ApjwG2",
}

PACKAGES = find_packages(exclude=["tests", "tests.*"])

REQUIRES = [
    "aiohttp==3.7.4.post0",
    "astral==2.2",
    "async_timeout==3.0.1",
    "attrs==21.2.0",
    "awesomeversion==21.2.3",
    'backports.zoneinfo;python_version<"3.9"',
    "bcrypt==3.1.7",
    "certifi>=2020.12.5",
    "ciso8601==2.1.3",
    "httpx==0.18.0",
    "jinja2>=2.11.3",
    "PyJWT==1.7.1",
    # PyJWT has loose dependency. We want the latest one.
    "cryptography==3.3.2",
    "pip>=8.0.3,<20.3",
    "python-slugify==4.0.1",
    "pyyaml==5.4.1",
    "requests==2.25.1",
    "ruamel.yaml==0.15.100",
    "voluptuous==0.12.1",
    "voluptuous-serialize==2.4.0",
    "yarl==1.6.3",
]



setup(
    name=PROJECT_PACKAGE_NAME,
    version="1.3",
    url=PROJECT_URL,
    project_urls=PROJECT_URLS,
    author=PROJECT_AUTHOR,
    author_email=PROJECT_EMAIL,
    packages=PACKAGES,
    include_package_data=True,
    zip_safe=False,
    install_requires=requirements,
    test_suite="tests",
    entry_points={"console_scripts": ["alpha-video = alpha_video.__main__"]},
)