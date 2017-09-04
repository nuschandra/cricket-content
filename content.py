import requests
from bs4 import BeautifulSoup
import mysql.connector
import test

requests.packages.urllib3.disable_warnings()

cnx=mysql.connector.connect(user='b1ffd2fe23b05d',password='efd23b14',
	host='us-cdbr-iron-east-03.cleardb.net',database='heroku_2202757061fad82')
cursor=cnx.cursor()
cricinfo='https://www.espncricinfo.com/ci/engine/match/index.html'

currentMatchPage = requests.get(cricinfo,verify=False)
currentMatchPageText = currentMatchPage.text

soup=BeautifulSoup(currentMatchPageText,"lxml")
allCurrentMatchTypes=soup.findAll('div',class_='match-section-head')
allCurrentMatchSections=soup.findAll('section',class_='matches-day-block')
delete_scores="DELETE FROM CURRENT_SCORES"
cursor.execute(delete_scores)	
delete_matches="DELETE FROM CURRENT_MATCHES"
cursor.execute(delete_matches)
cnx.commit()
index=0
for section in allCurrentMatchSections:
	match_type=allCurrentMatchTypes[index].find(text=True)
	if match_type is not None:
		match_type=match_type.strip()
	index+=1
	currentMatches=section.findAll('section',class_='default-match-block')
	for match in currentMatches:
		match_date=match.find('div',class_='match-info').find('span',class_='bold').find(text=True)
		if match_date is not None:
			print(match_date.strip())
			match_date=match_date.strip()

		match_status=match.find('div',class_='match-status').find('span',class_='bold').find(text=True)
		if match_status is not None:
			print(match_status.strip())
			match_status=match_status.strip()


		match_url=match.find('a').get('href')
		if match_url is not None:
			print(match_url)
			match_url=match_url.strip()
			match_url=match_url.replace('http://','https://')

		match_details=match.find('a').find(text=True)
		if match_details is not None:
			print(match_details)
			match_details=match_details.strip()

		team_one=match.find('div',class_='innings-info-1').find(text=True)
		if team_one is not None:
			print(team_one)
			team_one=team_one.strip()
		
		team_two=match.find('div',class_='innings-info-2').find(text=True)
		if team_two is not None:
			print(team_two)
			team_two=team_two.strip()
		print()
		if 'game/' in match_url:
			matchStringIndex=match_url.index('game/')			
		else:
			matchStringIndex=match_url.index('scorecard/')

		matchStringFirstSlash=int(match_url.find('/',matchStringIndex))
		matchStringIndex2=int(match_url.find('/',matchStringFirstSlash+1))
		match_id=int(match_url[matchStringFirstSlash+1:matchStringIndex2])
		print(match_id)
		add_match=("INSERT INTO CURRENT_MATCHES "
					"(MATCH_ID,TEAM_1,TEAM_2,MATCH_TYPE,MATCH_DETAILS,MATCH_URL,MATCH_DATE,MATCH_STATUS) "
					"VALUES (%s,%s,%s,%s,%s,%s,%s,%s)")
		match_info=(match_id,str(team_one),str(team_two),str(match_type),str(match_details),str(match_url),str(match_date),str(match_status))		
		cursor.execute(add_match,match_info)
		cnx.commit()
		test.get_scores(match_url,match_id,cnx)

cnx.close()

