# from pathlib import Path
from setuptools import setup, find_packages

# requirements = Path("requirements/main.in").read_text().splitlines()

setup(
    name="media_mgmt",
    version="0.1.0",
    packages=find_packages("src"),
    package_dir={"": "src"},
    include_package_data=True,
    install_requires=[
        "Click",
    ],
    entry_points={
        "console_scripts": [
            "mmgmt = mmgmt.cli:mmgmt",
        ],
    },
    # install_requires=requirements,
)
