
import pandas as pd

# identifying false negatives -- something buggy about this though
# clear example of false negative on 1/31/2019

notpassdf = pd.read_csv('not_passing.csv')
SOME_DATES = pd.unique(notpassdf['date'])

possible_missed_passes = pd.DataFrame(columns =['bird_ID', 'date', 'bird_played', 'key_pecked', 'time'])
for date in SOME_DATES:
	index_within_subset = 0
	subset = notpassdf[(notpassdf['date'] == date)] # & (notpassdf['time'] > 3)]
	# counter = subset[(subset['time'] > 3)].count()['time']
	# counter = (subset['time'] > 3).sum()
	counter = 0
	for index, row in subset.iterrows():
		if row['time'] > 3:
			counter += 1
		else:
			counter = 0

		if counter >= 4: 
			possible_pass = subset.iloc[index_within_subset -3 : index_within_subset + 1]

			print(subset.iloc[index_within_subset - 3: index_within_subset + 1])
			possible_missed_passes = pd.concat([possible_missed_passes, possible_pass], axis=0) # add this subset to passing 
		index_within_subset += 1
	# if there are more than four rows in this day that have more than 3 pulls, we should inspect to find false negatives 
	
possible_missed_passes.to_csv('possible_missed_passes.csv')