import pandas as pd

"""
Idea:

To separate passing tests from not passing tests,
all the necessary information should be in the data_summary_key.csv

this assumes < 3 pulls in any row for a given bird and given date should be filed into not pass
otherwise puts it into pass 

to filter false negatives within the notpass.csv, there is an additional file created
called possible_missed_passes.csv 
which contains all the subsets that may contain tests that passed but were 
miscategorized 

"""

df = pd.read_csv('data_summary_key.csv')

ALL_BIRDS = pd.unique(df['bird_ID'])
ALL_DATES = pd.unique(df['date'])



currentbird = 'bk83pi195'
currentdate = '12/11/2020'


def what_birds_today(date):
	""" what birds were played on a given date """ 
	subset =  list(set(df[df['date'] == date]['bird_ID']))
	subset.sort()
	return subset

def get_count_dict_for_subset(currentbird, currentdate):
	"""
	get counts for each male played by key pecked 
	"""

	counts = {} 
	subset = df[(df['bird_ID'] == currentbird) & (df['date'] == currentdate)]
	if subset.empty:
		return None 


	for index, row in subset.iterrows():
		key = str(row['bird_played']) + '_' + str(row['key_pecked'])
		if key in counts:
			counts[key] += 1 # if key is in counts 
		else:
			counts[key] = 1
	return counts 


def get_pecknumbers_for_subset(currentbird, currentdate):
	"""
	get key pecks for each male played by key pecked 
	"""

	pecks = {} 
	subset = df[(df['bird_ID'] == currentbird) & (df['date'] == currentdate)]
	if subset.empty:
		return None 


	for index, row in subset.iterrows():
		key = str(row['bird_played']) + '_' + str(row['key_pecked'])
		if key in pecks:
			
			pecks[key] += row['time']
			
		else:
			pecks[key] = row['time']
			
	return pecks 

'''
print("did they pull on each string?")
counts = get_count_dict_for_subset(currentbird, currentdate)
print(counts)

print("how many pecks")
print(get_pecknumbers_for_subset(currentbird, currentdate))
'''

print("What birds were played on 3/24/2017?")
print(what_birds_today('3/24/2017'))

example = get_pecknumbers_for_subset('2', '3/24/2017') # how many times they pulled for each key/bird combo
print("3/24/2017 peck counts for bird 2: ")
print(example)
notpass = False 
for key, value in example.items():
	if value < 3:
		# this bird date bird played combo does not pass (how do we get the other bird played?)
		notpass = True 
print("did this test pass? ")
if not notpass:
	print("No")
# is there any issue with always throwing an entire bird and date subset into not pass if there is a single entry with fewer than 3 pulls?

passing = pd.DataFrame(columns = ['bird_ID', 'date', 'bird_played', 'key_pecked'])
not_passing = pd.DataFrame(columns =['bird_ID', 'date', 'bird_played', 'key_pecked'])


odd_number_counter = 0
simple_pairs_counter = 0 
ALL_DATES.sort()
for date in ALL_DATES:
	# only loop over birds played on that date 
	birdlist = what_birds_today(date)
	if len(birdlist) % 2 == 1:
		odd_number_counter += 1
	if len(birdlist) == 2: 
		simple_pairs_counter += 1

	for bird in birdlist: 
		sub = df[(df['bird_ID'] == bird) & (df['date'] == date)] # subset with this bird and date 
		if len(sub['bird_played']) == 2:
			simple_pairs_counter += 1
		elif len(sub['bird_played']) % 2 == 1:
			odd_number_counter += 1

		count = get_count_dict_for_subset(bird, date) # whether each bird played is seen with each key 
		peck_dict = get_pecknumbers_for_subset(bird, date) # how many times they pulled for each key/bird combo


		notpass = False 
		for key, value in peck_dict.items():
			if value < 3:
				# this bird date bird played combo does not pass (how do we get the other bird played?)
				notpass = True 
		if notpass:
			not_passing = pd.concat([not_passing, sub], axis=0) # add this subset to not passing 
		else:
			passing = pd.concat([passing, sub], axis=0) # add this subset to passing 


print(peck_dict)
print(odd_number_counter)
print(simple_pairs_counter) 


# thoughts -- the day / bird combos with only two birds played are unambiguous 
# as a last resort, we could make passing and not passing with only these since they should be rock solid 
# any ambiguities come from multiple test situations

# in particular, this code is not robust to the case where one bird is played for a small amount of time
# in the beginning of the day and is not part of any actual test
# this will be automatically counted as a not pass if the bird pulls fewer than thrice for that bird 
# even if any subsequent tests for that bird on that day succeed 

# this code is also not robust to cases where a bird undergoes multiple tests in a day 
# but those tests do not all pass / do not all fail, as this automatically categorizes them by bird/date only

# an alternative approach (with its own tradeoffs) is to use bird_played in tandem with bird/date
# and only add rows to the final csvs if they are in the bird/date/bird played subset (ie using all three)
# the risk with this is shown by cases like 3/24/2017: we take half the test into pass, and half into not pass

# the only way I can think of to make this fully robust is to repurpose the determine_test_type_code
# so that any time we are removing a certain bird/date/bird played subset bc of < 3 pulls,
# we search within the broader bird/date subset for a bird that pairs with this bird to produce something other than a misfit
# however this is (obviously) complicated and may take a while both to implement and run 

passing.to_csv('passing.csv')
not_passing.to_csv('not_passing.csv')

