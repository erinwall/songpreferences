import pandas as pd
import numpy as np 

path = 'https://github.com/erinwall/songpreferences/raw/main/final_data_summary.csv'
#successful data summary csv
df = pd.read_csv(path)

by_bird_by_date = df.groupby(['bird_ID', 'date'])['bird_played'].apply(list).reset_index()

print(by_bird_by_date)

print(by_bird_by_date['bird_played'][0])

y = [by_bird_by_date['bird_played'][0][0]] + [by_bird_by_date['bird_played'][0][1]]

print(y)



listA = ['g32b89_UD', 'pi183y24_UD', 'r16y36', 'bl43p196_UD']
listB = ['bkor_UD', 'blk17_UD', 'bl11pu3_UD', 'bl4b13_UD']
listC = ['bl21pu11_FD', 'bl84gr17', 'bl80bk11_FD', 'bl31pi51_FD', 'bl74gy24_FD', 'bl71bl60_FD', 'bl63bk93_FD', 'bl87re02_FD', 'bl33ye35_FD', 'bl90pi15_FD', 'bl111gr09_FD', 'bl87pu80_FD', 'bl62or12_FD', 'bl49gy31_FD', 'bl61or11_FD', 'bl44pi74_FD', 'bl90or19_FD', 'bl43pi73_FD', 'bl58gr33_FD', 'bl100pu80_FD', 'bl34pu94_FD', 'bl86pi11_FD', 'bl65wh75_FD', 'bl14y6_FD', 'bl11pu3_FD', 'bl87bk3_FD', 'bl4b13_FD', 'pu55bl08_FD', 'bl17pi39_FD']
listD = ['bl21pu11_UD', 'bl80bk11_UD', 'bl31pi51_UD', 'bl74gy24_UD', 'bl71bl60_UD', 'bl63bk93_UD', 'bl87re02_UD', 'bl33ye35_UD', 'bl90pi15_UD', 'bl111gr09_UD', 'bl87pu80_UD', 'bl62or12_UD', 'bl49gy31_UD', 'bl61or11_UD', 'bl44pi74_UD', 'bl90or19_UD', 'bl43pi73_UD', 'bl58gr33_UD', 'bl100pu80_UD', 'bl34pu94_UD', 'bl86pi11_UD', 'bl65wh75_UD', 'bl14y6_UD', 'bl11pu3_UD', 'bl87bk3_UD', 'bl4b13_UD', 'pu55bl08_UD', 'bl17pi39_UD']
listE = ['bkor_FD']  
listF = ['bkor_UD']
listG = ['blk17_FD']
listH = ['blk17_UD']
listI = ['yelred_FD']
listJ = ['yelred_UD']
listK = ['yelgrn_FD']
listL = ['yelgrn_UD']
listM = ['pu35pu36_UD', 'y40b7_UD']
listN = ['bl1p1_UD', 'bl17y31_UD']
listO = ['bl32gy22_UD', 'bl17bl57_UD', 'bl17bl57_FD']
listP = ['pu21pu22_UD', 'pu17pu18_UD']
listQ = ['b85w66', 'pu54bl21']
listU = ['p3y3', 'pu46w46']



def determine_test_type(song_pair):
  test_type = None

  # note: probably a better way to do this, but too late now

  if ((song_pair[0] in listA and song_pair[1] in listB) or (song_pair[1] in listA and song_pair[0] in listB)):
    test_type = 'con vs het'
  #elif song_pair[0] not in listA:
   # test_type = 'some other test'
  elif (song_pair[0] in listC and song_pair[1] in listC):
    test_type = 'fam vs unfam'
  elif ((song_pair[0] in listC and song_pair[1] in listD) or (song_pair[1] in listC and song_pair[0] in listD)):
    test_type = 'familiar FD vs UD'
  elif ((song_pair[0] in listE and song_pair[1] in listF) or (song_pair[1] in listE and song_pair[0] in listF)):
     test_type = 'unfamiliar FD vs UD - bkor' 
  elif ((song_pair[0] in listG and song_pair[1] in listH) or (song_pair[1] in listG and song_pair[0] in listH)):
     test_type = 'unfamiliar FD vs UD - blk17' 
  elif ((song_pair[0] in listI and song_pair[1] in listJ) or (song_pair[1] in listI and song_pair[0] in listJ)):
     test_type = 'unfamiliar FD vs UD - yelred' 
  elif ((song_pair[0] in listK and song_pair[1] in listL) or (song_pair[1] in listK and song_pair[0] in listL)):
     test_type = 'unfamiliar FD vs UD - yelgrn' 
  elif (song_pair[0] in listM and song_pair[1] in listM):
    test_type = 'pair2'
  elif (song_pair[0] in listN and song_pair[1] in listN):
    test_type = 'pair3'
  elif (song_pair[0] in listO and song_pair[1] in listO):
    test_type = 'pair4'
  elif (song_pair[0] in listP or song_pair[1] in listP):
    test_type = 'tutor vs mate'
  elif (song_pair[0] in listQ and song_pair[1] in listQ):
    test_type = 'pair1'
  elif (song_pair[0] in listU and song_pair[1] in listU):
    test_type = 'pair5'
  else:
    test_type = 'misfit'
  return test_type


#test_types =  np.empty(len(by_date))

test_types = []
for i in range(len(by_bird_by_date)):
  # original:  y = [by_bird_by_date[i][0]] + [by_bird_by_date[i][1]]

  current_list = by_bird_by_date['bird_played'][i]
  if len(current_list) == 2:

    y = [current_list[0]] + [current_list[1]]
    test_type = determine_test_type(y)
    test_types += [test_type] 


  # this is a little ugly and vERY hacky, but it SEEMS to work?
  # maybe there's a way to just cycle through the permutations when we have a bunch of tests 

  elif len(current_list) == 3:

    sublist = []
    y = [current_list[0]] + [current_list[1]]
    test_type = determine_test_type(y)

    sublist += [test_type] 
    y = [current_list[1]] + [current_list[2]]
    test_type = determine_test_type(y)

    sublist += [test_type] 
    y = [current_list[0]] + [current_list[2]]
    test_type = determine_test_type(y)

    sublist += [test_type] 
    test_types += [sublist]

  elif len(current_list) == 4:
    sublist = []

    y = [current_list[0]] + [current_list[1]]
    test_type = determine_test_type(y)

    sublist += [test_type] 
    y = [current_list[2]] + [current_list[3]]
    test_type = determine_test_type(y)
    
    sublist += [test_type] 
    y = [current_list[1]] + [current_list[2]]
    test_type = determine_test_type(y)

    sublist += [test_type] 
    y = [current_list[0]] + [current_list[3]]
    test_type = determine_test_type(y)

    sublist += [test_type] 
    y = [current_list[0]] + [current_list[2]]
    test_type = determine_test_type(y)
    
    sublist += [test_type] 
    y = [current_list[1]] + [current_list[3]]
    test_type = determine_test_type(y)

    sublist += [test_type] 
    test_types += [sublist]

  else:
    test_types += [None]
    pass 


print(test_types)

by_bird_by_date['test type'] = test_types
print(by_bird_by_date)
by_bird_by_date.to_csv('data_summary_testtypes1.csv')
