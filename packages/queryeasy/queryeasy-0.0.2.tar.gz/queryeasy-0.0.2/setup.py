import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="queryeasy",
    version="0.0.2",
    author="Dheeraj Alimchandani",
    author_email="dheeraj.alim@gmail.com",
    description="Execute SQL queries on data present in CSV or Excel files. Also allows to generate the query"
                " output files.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dheerajalim/queryeasy",
    project_urls={
        "Bug Tracker": "https://github.com/dheerajalim/queryeasy/issues",
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries",
        "Topic :: Desktop Environment",
        "Environment :: Console",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    install_requires=[
        "pandas ~= 1.2",
        "xlrd == 1.2.0",
        "xlwt == 1.2.0",
        "openpyxl ~= 3.0",
        "sqlalchemy ~= 1.4",
    ],
    py_modules=["queryeasy"],
    entry_points={"console_scripts": ["queryeasy = queryeasy:_run_query"]},
)
