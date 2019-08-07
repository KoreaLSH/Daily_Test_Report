#!/bin/bash
# 1. crontab에 의해 이 스크립트가 실행된다.
# 2. report.py 파일 실행.
# 3. 오늘 데일리 테스트가 수행됐었다면, pandoc으로 report.md를 html로 변환해서 이메일로 보낸다.
# 4. 데일리 테스트가 수행되지 않았다면 notest.html 파일의 내용을 mutt 명령어로 보낸다.
export HOME=/home/qa

today=$(date +"%y-%m-%d")

python $HOME/work/report/test.py

ref=`python $HOME/work/report/test.py`

if [ $ref="TEST" ]; then
	pandoc $HOME/work/report/test.md -f markdown -t html -s -o $HOME/work/report/$today.html
	mutt -s "$today Daily Test Report" -e "set content_type=text/html" machintern@gmail.com < $HOME/work/report/$today.html
else # $ref = "NOTEST"
	mutt -s "$today Daily Test Report" -e "set content_type=text/html" machintern@gmail.com < $HOME/work/report/notest.html
fi


