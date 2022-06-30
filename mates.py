import pandas as pd 


mates = pd.read_csv('Bird_ID_FamMale_ID.csv')



# making dictionary 
def mates_dict(mates):
	mate_dictionary = {}

	males = mates['FamMale_ID']
	females = mates['Bird_ID']

	for i, femaleID in enumerate(females):
		maleID = males[i]
		if maleID not in mate_dictionary:
			mate_dictionary[maleID] = []

		mate_dictionary[maleID] += [femaleID]
	return mate_dictionary


# using it 
def check_if_familiar(current_bird, current_male):
	mate_dictionary = mates_dict(mates)
	if current_bird in mate_dictionary[current_male]:
		return True # print("yep, they are fmailiar ")
	else:
		return False 


def main():
	current_bird = 'bl46pi46'
	current_male = 'bl17gr84'

	print(check_if_familiar(current_bird, current_male))

if __name__ == '__main__':
	main()