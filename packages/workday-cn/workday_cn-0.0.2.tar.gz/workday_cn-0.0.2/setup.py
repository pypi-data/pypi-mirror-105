import setuptools

setuptools.setup(
    name="workday_cn",
    version="0.0.2",
    author="lovic",
    author_email="",
    description="workday detection",
    long_description="",
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
        "Operating System :: POSIX :: Linux",
    ],
    # install_requires=[
    #     'pymysql',
    #     'pandas',
    #     'requests',
    #     'sqlalchemy'
    # ],
    python_requires='>=3.6'
)