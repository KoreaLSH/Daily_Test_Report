#!/bin/bash
# 1. crontab에 의해 이 스크립트가 실행된다.
# 2. report.py 파일 실행.
# 3. pandoc으로 report.md를 html로 변환한다. 
# 4. report.html 파일의 내용을 mutt 명령어로 보낸다.
today=$(date +"%y-%m-%d")

python report.py

ref=`python report.py`

if [ $ref = "TEST" ]; then
	pandoc report.md -f markdown -t html -s -o $today.html
	mutt -s "$today Daily Test Report" -e "set content_type=text/html" machintern@gmail.com < $today.html
else
	mutt -s "$today Daily Test Report" -e "set content_type=text/html" machintern@gmail.com < notest.html
fi


