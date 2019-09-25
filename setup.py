from setuptools import setup, find_packages

with open("requirements.in") as f:
    install_requires = [line for line in f if line and line[0] not in "#-"]

setup(
    name="pycron",
    version="0.2",
    url="https://github.com/vjgarcera/pycron",
    author="Tiko JG",
    author_email="vjgarcera@gmail.com",
    download_url="https://github.com/vjgarcera/pycron",
    description="Python implementation of Cron daemon",
    packages=find_packages(),
    install_requires=install_requires,
    entry_points={"console_scripts": "pycron=pycron.pycron:main"}
)
