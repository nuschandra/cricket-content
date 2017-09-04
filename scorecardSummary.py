def batsmanSummary(currentBatsmen,batsmanName,batsmanRuns,batsmanStrikeRate,index):
	name=[None]*2
	batsmanRunsScored=[None]*2
	batsmanBallsFaced=[None]*2
	strikeRate=[None]*2
	for idx,player in enumerate(currentBatsmen):
		runs=player.findNext('span').findNext('span').findNext('span').findNext('span')
		name[idx]=player.find(text=True).strip()
		batsmanRunsScored[idx]=runs.find(text=True).strip()
		balls=runs.findNext('span').findNext('span')
		batsmanBallsFaced[idx]=balls.find(text=True).strip()
		if(batsmanBallsFaced[idx]!=0):
			strikeRate[idx]=float((int(batsmanRunsScored[idx])/int(batsmanBallsFaced[idx]))*100)
		else:
			strikeRate[idx]=float(0)
		if(idx==1):
			if(batsmanRunsScored[idx]>batsmanRunsScored[idx-1]):
				batsmanName[index]=name[idx]
				batsmanRuns[index]=batsmanRunsScored[idx]+'('+batsmanBallsFaced[idx]+')'
				batsmanStrikeRate[index]=strikeRate[idx]

			elif(batsmanRunsScored[idx]==batsmanRunsScored[idx-1]):
				if(strikeRate[idx]>=strikeRate[idx-1]):
					batsmanName[index]=name[idx]
					batsmanRuns[index]=batsmanRunsScored[idx]+'('+batsmanBallsFaced[idx]+')'
					batsmanStrikeRate[index]=strikeRate[idx]
		else:
			batsmanName[index]=name[idx]
			batsmanRuns[index]=batsmanRunsScored[idx]+'('+batsmanBallsFaced[idx]+')'
			batsmanStrikeRate[index]=strikeRate[idx]


def bowlerSummary(currentBowlers,bowlerName,bowlerOvers,bowlerRuns,bowlerWickets,bowlerEco,index):
	name=[None]*2
	overs=[None]*2
	runsGiven=[None]*2
	wickets=[None]*2
	economyRate=[None]*2
	for idx,player in enumerate(currentBowlers):
		name[idx]=player.find(text=True).strip()
		wicket=player.findNext('span').findNext('span')
		wickets[idx]=wicket.find(text=True).strip()
		runs=wicket.findNext('span').findNext('span')
		runsGiven[idx]=runs.find(text=True).strip()
		over=runs.findNext('span').findNext('span')
		overs[idx]=over.find(text=True).strip()
		economyRate[idx]=float(float(runsGiven[idx])/float(overs[idx]))
		if(idx==1):
			if(wickets[idx]>wickets[idx-1]):
				bowlerName[index]=name[idx]
				bowlerOvers[index]=overs[idx]
				bowlerRuns[index]=runsGiven[idx]
				bowlerWickets[index]=wickets[idx]
				bowlerEco[index]=economyRate[idx]

			elif(wickets[idx]==wickets[idx-1]):
				if(economyRate[idx]<=economyRate[idx-1]):
					bowlerName[index]=name[idx]
					bowlerOvers[index]=overs[idx]
					bowlerRuns[index]=runsGiven[idx]
					bowlerWickets[index]=wickets[idx]
					bowlerEco[index]=economyRate[idx]
		else:
			bowlerName[index]=name[idx]
			bowlerOvers[index]=overs[idx]
			bowlerRuns[index]=runsGiven[idx]
			bowlerWickets[index]=wickets[idx]
			bowlerEco[index]=economyRate[idx]