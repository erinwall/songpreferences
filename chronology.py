import pandas as pd
import numpy as np 

"""
code for processing raw data to use in determining overcounted or undercounted tests 

ie this code should answer the question 
'were these two songs tested on this day?''


important question: were there ever any 3-song tests? 


"""



def convert_time(timestamp):
	splittime = timestamp.split(':')
	return int(splittime[0])*3600 + int(splittime[1])*60 + int(splittime[2])


# iterate through rows
# SHOULD AUTO RESET FOR NEW DATE
def was_test_done(raw, songdict, indate, male1, male2, whichbird):
	
	try:
		result = test_or_not[indate + ' ' + male1 + ' ' + male2]
		if timediff > threshold:
			print("These two songs were part of a test that lasted ", result, " seconds")
		else:
			print("These songs were only played against each other for ", result, " seconds")
	except KeyError:
		print("These two songs were not tested on ", indate)


# try for a given date and song pair (eventually map to male ID)

def main():



	males_and_their_songs = pd.read_csv('songsplayed_sorted_forcode.csv')
	
	# males_and_their_songs['song_played']

	# males_and_their_songs['bird_played']

	bird_song_lists = males_and_their_songs.groupby(['bird_played'])['song_played'].apply(list).reset_index()
	
	print(bird_song_lists)

	# populate dictionary of bird to song list pairs 
	birdsong_dict = {}
	
	# version 1
	# bird_song_list_males = bird_song_lists['bird_played']
	# bird_song_list_songs = bird_song_lists['song_played']
	'''
	for bird in pd.unique(bird_song_list_males):
		print(bird)
		birdsong_dict[bird] = [] # initialize to empty list 
		for songlist in bird_song_lists['song_played']:
			birdsong_dict[bird] += songlist # add each song list (may have redundant stimuli)
	'''


	# version 2
	for index, row in bird_song_lists.iterrows():
		thisbird = row['bird_played']
		birdsong_dict[thisbird] = []
		thissonglist = row['song_played']
		birdsong_dict[thisbird] += thissonglist

	
	print(birdsong_dict['blk17_UD'])
	

	# reverse dictionary 

	songs_to_bird = {}
	for k, v in birdsong_dict.items():
		for element in v:
			songs_to_bird[element] = k 

	print(songs_to_bird)

	raw = pd.read_csv("combined-csv-files_cleaned.csv")
	print(raw.head())
	


	# remove keypeck events -- key pecked should not matter, only which songs are being played 
	raw = raw[raw['song_played'] != 'keypeck event']
	print(raw)
	print(len(raw))




	# making test or not dictionary 

	test_or_not = {}
	threshold = 300    # how many seconds do we consider a test ?
	changefirst = True # which slot to change first
	first = None
	second = None
	date = None
	input_date = '11/26/2020'
	first_song = 'bl43p196_UD'
	second_song = 'bl4b13_UD'
	bird = 'bk83pi195'
	
	# filter down to this date and this bird 
	# NOTE: filtering prematurely here risks time jumps where other songs were played, this may not work 
	# raw = raw[raw['date'] == input_date]
	# raw = raw[raw['bird_ID'] == whichbird]



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
	
		if row['bird_ID'] == bird:

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
					
					if timediff > threshold:
						# storing a dictionary of whether [date, first song, second song] was really a test 
						test_or_not[str(date) + " " + str(first) + " " + str(second)] = timediff # True
					else:
						test_or_not[str(date) + " " + str(first) + " " + str(second)] = timediff # False 
					if changefirst == True:
						first = male
						changefirst = False
					else:
						second = male
						changefirst = True
					print(first)
					print(second)
					date = row['date']
					 

			count += 1
			

	# need to save test_or_not 
	print(test_or_not)

	# test_or_not = was_test_done(raw, songs_to_bird, input_date, first_song, second_song, bird)

	print(test_or_not[str(input_date) + " " + str(first_song) + " " + str(second_song)])




	
	

if __name__ == '__main__':
	main()




'''

code graveyard 



	# alt vers assuming boolean return val
	if result:
		print("These two songs comprised a test (success state unknown) on ", input_date)
	else:
		print("These songs were not tested on ", input_date)
'''
