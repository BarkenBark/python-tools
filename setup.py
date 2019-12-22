import setuptools

with open("README.md", "r") as file:
	long_description = file.read()

setuptools.setup(
	name="barktools",
	version="0.0.1",
	entry_points={
		"console_scripts": [
			"index_files = scripts.index_files:main"
			]
	},
	author="Oscar Bark",
	author_email="kurshid.ognianov@protonmail.com",
	description="Package containing various useful python modules and scripts",
	long_description=long_description,
	long_description_content_type="text/markdown",
	url="https://github.com/BarkenBark/python-tools",
	packages=['barktools', 'scripts'],
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent"
		],
	python_requires=">=3.6"
)