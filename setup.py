from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in human_resource/__init__.py
from human_resource import __version__ as version

setup(
	name="human_resource",
	version=version,
	description="TO manage employee issues and etc.",
	author="Shaima\'a Khashan",
	author_email="sh.khwork2020@gmil.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
