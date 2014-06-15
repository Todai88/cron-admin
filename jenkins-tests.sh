#!/bin/sh

source  ~/venvs/cronreader/bin/activate

# pip install --quiet -U -r requirements.txt
pip install  .
pip install --quiet -r requirements-test.txt

nosetests -v --with-xunit --with-xcoverage --cover-package=nlppe --cover-erase

pylint -d E1102,E0611,C0103,C0111,C0301,C0303,R0201,R0903,R0904,R0914,W0612 -f parseable reader/*.py | tee pylint.out
