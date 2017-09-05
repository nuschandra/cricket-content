import requests
from bs4 import BeautifulSoup
import scorecardSummary
requests.packages.urllib3.disable_warnings()

def get_scores(matchUrl,matchId,cnx):
	currentMatchPage = requests.get(matchUrl,verify=False)
	currentMatchPageText = currentMatchPage.text
	soup=BeautifulSoup(currentMatchPageText,"lxml")
	cursor=cnx.cursor()
	matchCompetitors=soup.findAll('div',class_='team__content')
	teamScores=[None]*2
	index=0
	for teams in matchCompetitors:
		team=teams.find('span',class_='long-name').find(text=True).strip()
		scores=teams.find('div',class_='score-container')
		if scores is not None:
			overs=scores.find('span',class_='over')
			if(overs is not None):
				overs=scores.find('span',class_='over').find(text=True).strip()
				teamScores[index]=team+" "+scores.find(text=True).strip()+overs
			else:
				if(scores.find(text=True) is not None):
					teamScores[index]=team+" "+scores.find(text=True).strip()
		print(teamScores[index])
		index+=1
	currentPlayers=soup.findAll('div',class_=['stat-container batsmen','stat-container bowler'])
	if(len(currentPlayers)>0):
		currentBatsmen=currentPlayers[0].findAll('div',class_='player')
		currentBowlers=currentPlayers[1].findAll('div',class_='player')
		batsmanName=[None]*2
		batsmanRuns=[None]*2
		batsmanFoursSixes=[None]*2
		batsmanStrikeRate=[None]*2
		index=0
		for batsman in currentBatsmen:
			batsmanName[index]=batsman.find('div',class_='player-name').find(text=True).strip()
			batsmanRuns[index]=batsman.find('div',class_='runs').find(text=True).strip()
			batsmanFoursSixes[index]=batsman.find('div',class_='runs').find('span').find(text=True).strip()
			ballsBracket=int(batsmanRuns[index].find('('))
			ballsBracket2=int(batsmanRuns[index].find(')'))
			batsmanRunsScored=int(batsmanRuns[index][:ballsBracket])
			batsmanBallsFaced=int(batsmanRuns[index][ballsBracket+1:ballsBracket2])
			if(batsmanBallsFaced!=0):
				batsmanStrikeRate[index]=float((batsmanRunsScored/batsmanBallsFaced)*100)
			else:
				batsmanStrikeRate[index]=float(0)

			index+=1

		bowlerName=[None]*2
		bowlerOvers=[None]*2
		bowlerMaidens=[None]*2
		bowlerRuns=[None]*2
		bowlerWickets=[None]*2
		bowlerEco=[None]*2
		index=0
		for bowlers in currentBowlers:
			bowlerStats=bowlers.findAll('span',class_='value')
			bowlerName[index]=bowlers.find('div',class_='player-name').find(text=True).strip()
			bowlerOvers[index]=float(bowlerStats[0].find(text=True).strip())
			bowlerMaidens[index]=int(bowlerStats[1].find(text=True).strip())
			bowlerRuns[index]=int(bowlerStats[2].find(text=True).strip())
			bowlerWickets[index]=int(bowlerStats[3].find(text=True).strip())
			bowlerEco[index]=float(bowlerStats[4].find(text=True).strip())
			index+=1

		add_scores=("INSERT INTO CURRENT_SCORES "
					"(MATCH_ID, TEAM_ONE_SCORE,TEAM_TWO_SCORE,BATSMAN_ONE_NAME, BATSMAN_TWO_NAME, BATSMAN_ONE_SCORE, BATSMAN_TWO_SCORE, BATSMAN_ONE_BOUNDARIES, BATSMAN_TWO_BOUNDARIES, BATSMAN_ONE_SR, BATSMAN_TWO_SR, BOWLER_ONE_NAME, BOWLER_TWO_NAME, BOWLER_ONE_OVERS, BOWLER_TWO_OVERS, BOWLER_ONE_MAIDENS, BOWLER_TWO_MAIDENS, BOWLER_ONE_RUNS, BOWLER_TWO_RUNS, BOWLER_ONE_WICKETS, BOWLER_TWO_WICKETS, BOWLER_ONE_ECO, BOWLER_TWO_ECO) "
					"VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)")
		scores_info=(matchId,str(teamScores[0]),str(teamScores[1]),str(batsmanName[0]),str(batsmanName[1]),str(batsmanRuns[0]),str(batsmanRuns[1]),str(batsmanFoursSixes[0]),str(batsmanFoursSixes[1]),batsmanStrikeRate[0],batsmanStrikeRate[1],str(bowlerName[0]),str(bowlerName[1]),bowlerOvers[0],bowlerOvers[1],bowlerMaidens[0],bowlerMaidens[1],bowlerRuns[0],bowlerRuns[1],bowlerWickets[0],bowlerWickets[1],bowlerEco[0],bowlerEco[1])
		cursor.execute(add_scores,scores_info)
		cnx.commit()
		return
	else:
		currentInnings=soup.findAll('article',class_='sub-module current-inning')
		batsmanName=[None]*2
		batsmanRuns=[None]*2
		batsmanFoursSixes=[None]*2
		batsmanStrikeRate=[None]*2

		bowlerName=[None]*2
		bowlerOvers=[None]*2
		bowlerMaidens=[None]*2
		bowlerRuns=[None]*2
		bowlerWickets=[None]*2
		bowlerEco=[None]*2
		if(len(currentInnings)>0):
			currentPlayers=currentInnings[0].findAll('a',href=True)
			noOfPlayers=len(currentPlayers)
			if(noOfPlayers>0):
				currentBatsmen=currentPlayers[0:int(noOfPlayers/2)]
				currentBowlers=currentPlayers[int(noOfPlayers/2):noOfPlayers]
				index=0
				for player in currentBatsmen:
					batsmanName[index]=player.find(text=True).strip();
					runs=player.findNext('td')
					batsmanRunsScored=int(runs.find(text=True).strip())
					balls=runs.findNext('td')
					batsmanBallsFaced=int(balls.find(text=True).strip())
					batsmanRuns[index]=runs.find(text=True).strip()+'('+balls.find(text=True).strip()+')'
					fours=balls.findNext('td')
					batsmanFours=fours.find(text=True).strip()
					sixes=fours.findNext('td')
					batsmanSixes=sixes.find(text=True).strip()
					batsmanFoursSixes[index]=batsmanFours+"x4 - "+batsmanSixes+"x6"
					if(batsmanBallsFaced!=0):
						batsmanStrikeRate[index]=float((batsmanRunsScored/batsmanBallsFaced)*100)
					else:
						batsmanStrikeRate[index]=float(0)
					index+=1

				index=0
				for player in currentBowlers:
					bowlerName[index]=player.find(text=True).strip();
					overs=player.findNext('td')
					bowlerOvers[index]=float(overs.find(text=True).strip())
					maidens=overs.findNext('td')
					bowlerMaidens[index]=int(maidens.find(text=True).strip())
					runs=maidens.findNext('td')
					bowlerRuns[index]=int(runs.find(text=True).strip())
					wickets=runs.findNext('td')
					bowlerWickets[index]=int(wickets.find(text=True).strip())
					eco=wickets.findNext('td')
					bowlerEco[index]=float(eco.find(text=True).strip())
					print(bowlerName[index])
					print(bowlerOvers[index])
					print(bowlerMaidens[index])
					print(bowlerRuns[index])
					print(bowlerWickets[index])
					print(bowlerEco[index])
					index+=1
				add_scores=("INSERT INTO CURRENT_SCORES "
					"(MATCH_ID, TEAM_ONE_SCORE,TEAM_TWO_SCORE,BATSMAN_ONE_NAME, BATSMAN_TWO_NAME, BATSMAN_ONE_SCORE, BATSMAN_TWO_SCORE, BATSMAN_ONE_BOUNDARIES, BATSMAN_TWO_BOUNDARIES, BATSMAN_ONE_SR, BATSMAN_TWO_SR, BOWLER_ONE_NAME, BOWLER_TWO_NAME, BOWLER_ONE_OVERS, BOWLER_TWO_OVERS, BOWLER_ONE_MAIDENS, BOWLER_TWO_MAIDENS, BOWLER_ONE_RUNS, BOWLER_TWO_RUNS, BOWLER_ONE_WICKETS, BOWLER_TWO_WICKETS, BOWLER_ONE_ECO, BOWLER_TWO_ECO) "
					"VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)")
				scores_info=(matchId,str(teamScores[0]),str(teamScores[1]),str(batsmanName[0]),str(batsmanName[1]),str(batsmanRuns[0]),str(batsmanRuns[1]),str(batsmanFoursSixes[0]),str(batsmanFoursSixes[1]),batsmanStrikeRate[0],batsmanStrikeRate[1],str(bowlerName[0]),str(bowlerName[1]),bowlerOvers[0],bowlerOvers[1],bowlerMaidens[0],bowlerMaidens[1],bowlerRuns[0],bowlerRuns[1],bowlerWickets[0],bowlerWickets[1],bowlerEco[0],bowlerEco[1])
				cursor.execute(add_scores,scores_info)
				cnx.commit()
				return
			else:
				return
		else:
			currentSummary=soup.findAll('article',class_='sub-module scorecard-summary')
			if(len(currentSummary)>0):
				currentPlayers=currentSummary[0].findAll('a',href=True)
				noOfPlayers=len(currentPlayers)
				firstInnings=currentPlayers[0:int(noOfPlayers/2)]
				secondInnings=currentPlayers[int(noOfPlayers/2):noOfPlayers-1]
				currentBatsmen=firstInnings[0:2]
				currentBowlers=firstInnings[2:4]
				scorecardSummary.batsmanSummary(currentBatsmen,batsmanName,batsmanRuns,batsmanStrikeRate,0)
				scorecardSummary.bowlerSummary(currentBowlers,bowlerName,bowlerOvers,bowlerRuns,bowlerWickets,bowlerEco,0)

				currentBatsmen=secondInnings[0:2]
				currentBowlers=secondInnings[2:4]
				scorecardSummary.batsmanSummary(currentBatsmen,batsmanName,batsmanRuns,batsmanStrikeRate,1)
				scorecardSummary.bowlerSummary(currentBowlers,bowlerName,bowlerOvers,bowlerRuns,bowlerWickets,bowlerEco,1)
				print(bowlerName[0])
				print(bowlerName[1])
				add_scores=("INSERT INTO CURRENT_SCORES "
					"(MATCH_ID, TEAM_ONE_SCORE,TEAM_TWO_SCORE,BATSMAN_ONE_NAME, BATSMAN_TWO_NAME, BATSMAN_ONE_SCORE, BATSMAN_TWO_SCORE, BATSMAN_ONE_BOUNDARIES, BATSMAN_TWO_BOUNDARIES, BATSMAN_ONE_SR, BATSMAN_TWO_SR, BOWLER_ONE_NAME, BOWLER_TWO_NAME, BOWLER_ONE_OVERS, BOWLER_TWO_OVERS, BOWLER_ONE_MAIDENS, BOWLER_TWO_MAIDENS, BOWLER_ONE_RUNS, BOWLER_TWO_RUNS, BOWLER_ONE_WICKETS, BOWLER_TWO_WICKETS, BOWLER_ONE_ECO, BOWLER_TWO_ECO) "
					"VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)")
				scores_info=(matchId,str(teamScores[0]),str(teamScores[1]),str(batsmanName[0]),str(batsmanName[1]),str(batsmanRuns[0]),str(batsmanRuns[1]),str(batsmanFoursSixes[0]),str(batsmanFoursSixes[1]),batsmanStrikeRate[0],batsmanStrikeRate[1],str(bowlerName[0]),str(bowlerName[1]),bowlerOvers[0],bowlerOvers[1],bowlerMaidens[0],bowlerMaidens[1],bowlerRuns[0],bowlerRuns[1],bowlerWickets[0],bowlerWickets[1],bowlerEco[0],bowlerEco[1])
				cursor.execute(add_scores,scores_info)
				cnx.commit()
				return

			else:
				return
