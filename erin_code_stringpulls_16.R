##Code to clean up, wrangle, and summarize string pull data. Adapted from Emma Hudgins & Erin Wall, by Erin Wall and Lee Wall. 2022
#read in the directory
rm(list=c(ls()))
setwd('C:/Users/erinw/Documents/mcgillexperiments/stringpulldata/csvstocombine_all') # change to directory where your file is located
library(dplyr)

# songs change keys at switch point
# number of days tested for each stimuli
# how many times pulled song b for each day
# did they pull 
#read in csv file
data<-read.csv("cleaned_merged_csvs.csv")
#remove column label rows
data<-subset(data, bird_ID!= "bird_ID")
# remove keypeck zero
data<-subset(data, key_pecked>0)
# remove keypeck event
data<-subset(data, song_played!= "keypeck event") # != is the not equal to operator, quotations are used for text so that R doesn't interpret it as a variable and interprets it as text
# remove duplicates - this will also remove rows if a bird pulls for the same stimuli more than once within the same second in same day (this does happen)
#data<-unique.data.frame(data)
#if needed run lapply (data, class) here and if key_pecked character, run data$key_pecked <- as.numeric(data$key_pecked)
lapply (data, class)
data$key_pecked <- as.numeric(data$key_pecked)
unique(data$bird_ID) # unique bird IDs
length(unique(data$bird_ID)) # how many unique bird IDs

#same with date
unique(data$date)
length(unique(data$date)) # how many unique dates
##list stimuli played 
unique(data$song_played)
length(unique(data$song_played))
song_played<-unique(data$song_played)
write.csv(song_played, file="songs_played.csv", row.names=F)


#old way#list all the birds played, using the prefixes used in the stimuli list
#birds<-c('norm_bl111gr09', "FD_bl111gr09", "norm_bl21pu11", "FD_bl21pu11", "norm_dir", "norm_undir", "p183y24", "yelred_undir", "yelred_dir", "bl11p3", "g32b89", "fatmaleround", "oldmaleround", "bl4b13", 'bl43p196', 'bl36p46', 'o102p102', 'norm_bl111gr09', "FD_bl111gr09", "norm_bl21pu11", "FD_bl21pu11", "norm_undir", "p183y24", "yelred_undir", "yelred_dir", "bl11p3", "g32b89", "fatmaleround", "oldmaleround", 'blor', 'dir', 'undir', 'pu17pu18', 'blk17dir', 'blk17undir', 'pu21pu22', "norm_bl4b13", 'bl43p196', 'pu55bl8', 'bl4b13', 'directed_bl14y6', 'norm_bl14y6', 'FD_bl87bk3','norm_bl87bk3', 'FD_bl65w75', 'norm_bl65w75', 'FD_bl86pi11','norm_bl86pi11', 'FD_bl94pu34' , 'norm_bl94pu34', 'FD_bl100pu80', 'norm_bl100pu80', 'FD_bl33y35', 'norm_bl33y35', 'FD_bl58gr33', 'norm_bl58gr33',  'FD_bl87re02', 'norm_bl87re02', 'FD_bl43pi73', 'norm_bl43pi73', 'FD_bl63bk93', 'norm_bl63bk93', 'FD_bl90or19', 'norm_bl90or19', 'FD_bl71bl60', 'norm_bl71bl60', 'FD_bl44pi74', 'norm_bl44pi74',  'FD_bl74gy24', 'norm_bl74gy24', 'FD_bl61or11', 'norm_bl61or11', 'FD_bl31pi51', 'norm_bl31pi51', 'FD_bl49gy31', 'norm_bl49gy31', 'FD_bl80bk11', 'norm_bl80bk11', 'FD_bl62or12', 'norm_bl62or12', 'FD_bl84gr17', 'norm_bl84gr17','FD_bl87pu80', 'norm_bl87pu80')
#new way#column name cases must match
#using the songs_played csv file, associate all the stimuli for an indivudal male (divided by FD and UD) with his ID. read in the csv that associates a males stimuli with his ID
bird_played<- read.csv ("songsplayed_sorted_forcode.csv")
#for R, all data point needs a new row, and all info for that point should be in that row (repeated)
data <- merge (data, bird_played, "song_played") #add all = TRUE if losing data after this step. reads the excel file that associates all stim for each bird with its unique name
write.csv(bird_played, file="birds_played.csv", row.names=F)

#dont use this anymore: data$bird_played<-unlist(sapply(data$song_played, FUN=function(x){which(sapply(1:length(birds), FUN=function(y){grepl(birds[y],x)})==T)}))
#dont use this either: data$bird_played<-birds[data$bird_played]
unique(data$song_played)
unique(data$bird_played)

length(unique(data$date)) 
#groups data to show bird_ID, date, stimuli (bird) played, and how many times the female pulled for that song on that day
data_summary<-data%>%group_by(bird_ID, date, bird_played)%>%summarise_at('key_pecked', length)
#this breaks it down to show what key was pecked for what stim, and how many times, on a given day. 
#note that this shows all pulls and does not yet only count pulls by the threshold of 3 times each key before the start and after the switch
#if you do not need the number of pulls calculated, but you just want to know if the test passed the criteria for a successful test, you could use the data_summary_key to determine if each bird_played was played on each key (each string) at least 3 times (each key) in a given test
data_summary_key<-data%>%group_by(bird_ID, date,bird_played,key_pecked)%>%summarise_at('time', length)
#use data_summary_key or data summary? to run in python for a table of all test attempts regardless of switch or threshold

#filtering needs to go here, since below loop currently only works on passing data. could probably adapt the loop to also look at not passing data by using if statements
#ideas: previous filtering created data frames that showed passing tests based on certain criteria, then created a data frame with all the data associated with the passing tests based on bird_ID and date in "pass" data frame. however this didn't fully work and also read in rows of data on the same day and same bird but from a different bird_played that didn't pass the criteria. maybe if we append "pass' to rows that show bird_played was played on both keys, or some way of bringing in the bird_played criteria in addition to bird ID and date. 

pass_pulls <- subset (data_summary_key, time>3)
pass1<-pass_pulls%>%group_by(bird_ID, date, bird_played)%>%summarise_at('key_pecked', length)
#notpass_switch<-subset(pass1, key_pecked<2)
pass_switch<-subset(pass1, key_pecked>=2)
notpass_switch<-subset(pass1, key_pecked<2) 
#this doesnt work, brings in data that it shouldnt: data_passed <- subset (data, date%in%pass_switch$date& bird_ID%in%pass_switch$bird_ID & bird_played%in%pass_switch$bird_played)
write.csv(pass_switch, file= "pass_pullsandswitch.csv", row.names=F) # THIS SEEMS TO WORK, RAN THROUGH PYTHON CODE AND CHECKED AGAINST TWO BIRDS EXAMPLES
write.csv(notpass_switch, file = "notpass_switch.csv", row.names=F)#use this to run in python to get table of all attempts where a bird_played was pulled more than 3 times but did not have a switch/didn't pull enough after the switch

#work with passing data for counts
data_pass<-subset(data,date%in%pass_switch$date& bird_ID%in%pass_switch$bird_ID)

#loop that counts up pulls after the thresholds (3 times each bird_played at start of test and after switch (sides))
#loop over each bird_ID
#combine bird id and date in a new column
pass_switch$bird_id_date<-paste(pass_switch$bird_ID,pass_switch$date, sep="_")
data_pass$bird_id_date<-paste(data_pass$bird_ID,data_pass$date, sep="_")
data_pass<-subset(data_pass, bird_id_date%in%pass_switch$bird_id_date)
#make new column with combination of key and bird_played
data_pass$keys_and_songs<-paste(data_pass$key_pecked,data_pass$bird_played, sep="_")


#loop over bird_id_date column
#initialize an empty final_data<-tibble(colname=NA, colname2=0)
##final_data<-as_tibble(data.frame(matrix(NA,nrow=0,ncol=length(colnames(bid_rows)))))
##colnames(final_data) <-colnames(bid_rows)

#use over passing data to count pulls after thresholds met
lapply(data_pass, class)
final_data<-tibble(bird_ID=NA, key_pecked=0, song_played=NA, date=NA, time=NA, bird_played=NA, bird_id_date=NA, keys_and_songs=NA, count=0)
for (bid in unique(data_pass$bird_id_date))
{
  bid_rows<-subset(data_pass,bird_id_date==bid)
  #figure out the starting row for the bird id and date
  bid_rows<-bid_rows%>%group_by(bird_id_date, time)
  #count up instances of each key and bird played combo
  bid_rows<-bid_rows%>%group_by(keys_and_songs)%>%mutate(count=row_number())
  #find index of second 3 (when they pass)
  switch1 <- which(bid_rows$count==3)[2]
  #bid_rows[which(bid_rows$count==3),] would give list of each count 3 including all info for each row
  #find index of third 1 (when it switches)
  switch2 <- which(bid_rows$count==1)[3]
  #find index of final 3 (when they pass again)
  switch3 <- which(bid_rows$count==3)[4]
  #if there are two tests in same day how do we look for these within second test? look for 6th 3, 6th 1, 8th 3? returns NA if not applicable
  switch4 <- nrow(bid_rows)
  if (length(which(bid_rows$count==3))>=6) {
    switch4 <- which(bid_rows$count==3)[6]
    if (length(which(bid_rows$count==3))>=8) {
      switch5 <- which(bid_rows$count==1)[6]
      switch6 <- which(bid_rows$count==3)[8]
      cleaned_subset <- bid_rows[c((switch4+1):(switch5-1), (switch6+1):nrow(bid_rows)),]
      #add these cleaned rows to an empty, new data file final_data<-bind_rows(cleaned_subset, final_data)
      final_data<-bind_rows(cleaned_subset, final_data)
      if (length(which(bid_rows$count==3))>=10){
        print ("more than two tests")
      }
    }}
  #remove rows before second 3 and between third 1 and final 3
  cleaned_subset <- bid_rows[c((switch1+1):(switch2-1), (switch3+1):switch4),]
  #add these cleaned rows to an empty, new data file final_data<-bind_rows(cleaned_subset, final_data)
  final_data<-bind_rows(cleaned_subset, final_data)
}
##write.csv to save to file
write.csv(final_data, file= "final_data.csv", row.names=F)

##summarize similiar to data_summary
final_data_summary<-final_data%>%group_by(bird_ID, date, bird_played)%>%summarise_at('key_pecked', length)
final_data_summary_key<-final_data%>%group_by(bird_ID, date,bird_played,key_pecked)%>%summarise_at('time', length)

##is the following necessary?
#this would remove rows where pulls less than 3, not using now: final_data_summary_key<-subset(final_data_summary_key, time>3)
final_pass<-final_data_summary_key%>%group_by(bird_ID, date)%>%summarise_at('key_pecked', length)
final_pass<-subset(final_pass, key_pecked>=4)
write.csv(final_data_summary_key, file="final_data_summary_key.csv", row.names=F)
write.csv(final_pass, file="final_passing_birds.csv", row.names=F)
write.csv(final_data_summary, file="final_data_summary.csv", row.names=F)