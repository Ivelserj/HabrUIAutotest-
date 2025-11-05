"""
Setup script for Habr UI Autotest project
"""
from setuptools import setup, find_packages

setup(
    name="habr-ui-autotest",
    version="1.0.0",
    description="UI autotest for Habr.com using Playwright, Python, Pytest, and Allure",
    packages=find_packages(),
    install_requires=[
        "playwright==1.40.0",
        "pytest==7.4.3",
        "pytest-playwright==0.4.3",
        "pytest-html==4.1.1",
        "pytest-xdist==3.5.0",
        "allure-pytest==2.13.2",
        "python-dotenv==1.0.0",
    ],
    python_requires=">=3.8",
)

