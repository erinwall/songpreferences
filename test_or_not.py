import pandas as pd
import numpy as np 

"""
Test or Not? 

this code should answer the question 
'were these two songs used together in a test for this bird on this day?''


important questions: 
were there ever any 3-song tests / simultaneous rotations of three stimuli? (currently assumes not)
were tests ever run overnight?  (currently assumes there were not)
what is the minimum length of a test?  (currently assumes 300 seconds = 5 minutes)


"""


def convert_time(timestamp):
	"""
	convert timestamp to a number of seconds 
	""" 

	splittime = timestamp.split(':')
	return int(splittime[0])*3600 + int(splittime[1])*60 + int(splittime[2])



def make_birdsong_dictionary(males_and_their_songs):

	"""
	given a csv of males and their associated songs, 
	populates a dictionary data structure for quick lookups  

	"""

	bird_song_lists = males_and_their_songs.groupby(['bird_played'])['song_played'].apply(list).reset_index()
	
	birdsong_dict = {}


	for index, row in bird_song_lists.iterrows():
		thisbird = row['bird_played']
		birdsong_dict[thisbird] = []
		thissonglist = row['song_played']
		birdsong_dict[thisbird] += thissonglist


	# reverse dictionary -- this produces a lookup table that maps a given song to the male that sings it 

	songs_to_bird = {}
	for k, v in birdsong_dict.items():
		for element in v:
			songs_to_bird[element] = k 

	return songs_to_bird 


def determine_test_times(raw, songs_to_bird, bird, input_date):

	"""
	this runs through the raw data and finds the time differences that define various tests
	it does this by logging the timestamp every time we see a bird that isn't part of the current pair
	with the assumption that this signals the end of the test defined by that pair 

	"""

	THRESHOLD = 300    # how many seconds do we consider a test ?
	changefirst = True # which slot to change first
	first = None
	second = None
	date = input_date

	test_or_not = {}
	count = 0 
	for index, row in raw.iterrows():
		print(index)
		if count == 0:
			test_start_time = row['time']
		try:
			male = songs_to_bird[row['song_played']]
		
		except KeyError:
			print("ERROR")
			print(row['song_played'], " ", row)
		
		# only check if we are on given bird 
		if row['bird_ID'] == bird:
			if date != input_date :
				break
			# we check if the encountered song is one of the current two
			# if it isn't, the old test is over
			if male != first:
				if male != second:
					test_end_time = row['time'] # if new song encountered, current test has ended 
					print(test_end_time)
					end_numeric = convert_time(test_end_time)
					start_numeric = convert_time(test_start_time)

					timediff = end_numeric - start_numeric  # find difference in seconds between times 
					test_start_time = test_end_time # reset test start time variable
					# find difference between time bird changed and test start time, change one to the other
					
					if timediff > THRESHOLD:
						# storing a dictionary of whether [bird, date, first song, second song] was really a test 
						test_or_not[str(bird) + " " + str(date) + " " + str(first) + " " + str(second)] = timediff # True
					else:
						test_or_not[str(bird) + " " + str(date) + " " + str(first) + " " + str(second)] = timediff # False 
					if changefirst == True:
						first = male
						changefirst = False
					else:
						second = male
						changefirst = True
					print(first)
					print(second)
					if row['date'] != date:
						date = row['date']

			count += 1
	return test_or_not 

def was_test_done(raw, songs_to_bird, bird, input_date, male1, male2):
	"""
	this just asks the dictionary produced by the function above whether there is an entry for 
	the given bird, date, and song pair
	if there isn't, they were not tested
	if there is, it outputs the number of seconds they appeared together 
	(note this will produce extraneous results on switches; for instance,
	if birds A and B are tested, then C and D, this will record an entry for B and C 
	because they are chronologically adjacent; difficult to avoid this without additional assumptions though)
	"""

	test_or_not = determine_test_times(raw, songs_to_bird, bird, input_date)
	key = bird + ' ' + input_date + ' ' + male1 + ' ' + male2 # assuming these are already strings!
	if key in test_or_not:
		result = test_or_not[key]
		if timediff > threshold:
			print("These two songs were part of a test that lasted ", result, " seconds")
			return True 
		else:
			print("These songs were only played against each other for ", result, " seconds")
			return False # assuming < threshold --> never a test 
	else:
		print("These two songs were not tested on ", input_date)
		return False 



def main():

	# read in raw data 
	raw = pd.read_csv("combined-csv-files_cleaned.csv")
	print(raw.head())

	# read in songs and males csv 
	males_and_their_songs = pd.read_csv('songsplayed_sorted_forcode.csv')

	# make birdsong lookup table 
	songs_to_bird = make_birdsong_dictionary(males_and_their_songs)

	# remove keypeck events -- key pecked should not matter, only which songs are being played 
	raw = raw[raw['song_played'] != 'keypeck event']


	
	input_date = '12/11/2020'
	male1 = 'bl43p196_UD'
	male2 = 'bl4b13_UD'
	thebird = 'bk83pi195'

	# key = str(thebird) + " " + str(input_date) + " " + str(male1) + " " + str(male2)
	# ignore first two parameters here for testing -- they are just the raw data and males -> songs csv, respectively 
	was_test_done(raw, songs_to_bird, thebird, input_date, male1, male2)



if __name__ == '__main__':
	main()