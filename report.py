#-*-coding:utf-8-*-
#한글 인코딩.

import string
import os 
import datetime
import sys
import json

def main ():
    	
	settings = ("fog-debug-linux","edge-debug-linux","cluster-debug-linux")
	report_md_path = os.getenv("HOME") + "/work/report/report.md"

	# 이메일의 본문으로 사용할 파일(report.md)의 내용을 lines에 읽어둔다.
	with open(report_md_path, "r" ) as f:
		lines = f.readlines()

	# 리스트의 6~12번 원소:  Daily test 출력 부분.	
	# 리스트의 18~24번 원소: 지난 테스트와의 차이를 출력하는 부분.
	daily_test_result_start_line = 6
	daily_test_result_end_line = 12
	differnce_start_line = 18
	differnce_end_line = 24 

	# 오늘 테스트를 수행 여부 확인을 위한 변수
	no_test_count = 0
	date_count = 0
   	
	# 오늘 날짜의 폴더를 찾기 위해 문자열 변수를  만든다.
	time_buffer = datetime.datetime.now()
	targetFolder_name = time_buffer.strftime('%Y-%m-%d')	

	for setting in settings:
		
		j=0
		k=0
	
		# 아래 for문의 line_list의 원소를 카운트하기 위함.
		if setting == "fog-debug-linux":
			edition_select = 1
		elif setting == "edge-debug-linux":
	   		edition_select = 2
		else:
			edition_select = 3
	
		# 오늘 Daily test 결과 파일(Summary.json)이 들어있는 디렉토리 경로명을 가진 변수 생성	
		setting_Folder_path = "/home/qa/QA/results/" + setting + "/"
		targetFolder_path = setting_Folder_path + targetFolder_name

		''' 가장 최근에 생성된 디렉토리와 그 직전의 디렉토리내의 summary.json 파일의 내용을 비교한다. 오늘 테스트 결과를 report.md에 반영한다. '''		
		if os.path.isdir(targetFolder_path) == True:
	
	    	# 오늘 생성된 daily test의 json 파일을 읽어온다.
			with open(targetFolder_path + "/summary.json","r") as f:
				targetFolder_json= json.load(f)
	
			# 오늘을 제외한 가장 최근 날짜의 jason 파일을 오늘 생성된 json 파일에서 읽어온다.
			lastTargetFolder_path = setting_Folder_path + targetFolder_json["lastTargetFolder"] 
			with open(lastTargetFolder_path + "/summary.json","r") as f:
				lastTargetFolder_json = json.load(f)
			
			# 날짜를 바꿔준다.
			if date_count==0:
				date_list = lines[2].split(" ")
				date_list[1] = targetFolder_json["targetFolder"].encode('utf-8') 
				lines[2] = date_list[0]+" "+date_list[1]+" "+date_list[2]+" "+date_list[3]+" "+date_list[4]
				date_count+=1
	
			# summary.json 파일 내의 'summary'의 값들을 리스트로 만든다.
			summary_list = list(targetFolder_json["summary"].values())
		
			# 리스트를 작성해서 여기에 오늘 결과값과 직전 테스트의 결과값의 차를 json파일 내의 summary 순서대로 저장해둠. 
			difference = []
			for i in targetFolder_json["summary"]:
				difference.append(targetFolder_json["summary"][i] - lastTargetFolder_json["summary"][i])
	
			for i in range(len(lines)):
    				 
				if (i >= daily_test_result_start_line) and (i <= daily_test_result_end_line):
					line_list = lines[i].split("|")
					line_list[edition_select] = str(summary_list[j])
					lines[i] = line_list[0]+"|"+line_list[1]+"|"+line_list[2]+"|"+line_list[3]+"\n"
					j+=1

				if (i >= differnce_start_line) and (i <= differnce_end_line):
					line_list = lines[i].split("|")
					line_list[edition_select] = str(difference[k])
					lines[i] = line_list[0]+"|"+line_list[1]+"|"+line_list[2]+"|"+ line_list[3]+"\n"
					k+=1
		else:
	    	# 오늘 날짜의 디렉토리가 없으면 report.md 파일 내의 현재 setting값과 관련된 부분에 NULL값을 넣어준다.
			# test를 수행하지 않은 횟수를 세기 위해 사용하는 변수.
			no_test_count += 1

			for i in range(len(lines)):

				if (i >= daily_test_result_start_line) and (i <= daily_test_result_end_line):	
					line_list = lines[i].split("|")
					line_list[edition_select] = 'NULL'
					lines[i] = line_list[0] +"|"+ line_list[1] +"|"+ line_list[2] +"|"+ line_list[3] + "\n"

				if (i >= differnce_start_line) and (i <= differnce_end_line):
					line_list = lines[i].split("|")
					line_list[edition_select] = 'NULL'
					lines[i] = line_list[0] +"|"+ line_list[1] +"|"+ line_list[2] +"|"+ line_list[3] + "\n"
	
	
	# Daily test를 전혀 하지 않은 경우
	if no_test_count >= 3:
		print("NOTEST")
		sys.exit()

	# 변경된 내용을 파일에 반영한다.
	with open(report_md_path, "w") as f:
		for buffer in lines:
			f.write(buffer)
		print("TEST")


if __name__ == '__main__':
	
	main()
