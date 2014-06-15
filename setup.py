import os
from setuptools import setup


# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name="cron-admin",
    version="0.0.1",
    author="Ian Wilson",
    author_email="ian@emotionai.com",
    description="Find when cron jobs will next run",
    keywords="python cron-admin cron run",
    url="https://github.com/emotionai/cron-admin",
    packages=['nextrun'],
    entry_points={
        "console_scripts":
            ['cron-admin = nextrun.__main__:main'],
    },
    package_dir={'nextrun': 'nextrun'},
    package_data={
        'nextrun': ['config/*cfg'],
    },
    data_files=[('', ['README.md'])],
    long_description=read('README.md'),
)
