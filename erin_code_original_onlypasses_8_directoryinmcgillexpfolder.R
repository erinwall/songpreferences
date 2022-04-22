rm(list=c(ls()))
setwd('C:/Users/erinw/Documents/mcgillexperiments/stringpulldata/csvstocombine') # change to directory where your file is located
library(dplyr)

# songs change keys at switch point
# number of days tested for each stimuli
# how many times pulled song b for each day
# did they pull 
data<-read.csv("combined-csv-files_cleaned.csv")
#remove column label rows
data<-subset(data, bird_ID!= "bird_ID")
# remove keypeck zero
data<-subset(data, key_pecked>0)
# remove keypeck event
data<-subset(data, song_played!= "keypeck event") # != is the not equal to operator, quotations are used for text so that R doesn't interpret it as a variable and interprets it as text
# remove duplicates - this will also remove rows if a bird pulls for the same stimuli more than once within the same second in same day (this does happen)
#data<-unique.data.frame(data)
unique(data$bird_ID) # unique bird IDs, something weird happens with output where its showing more than just bird IDs. 
length(unique(data$bird_ID)) # how many unique bird IDs

#same with date
unique(data$date) #same thing here where it shows more than dates
length(unique(data$date)) # how many unique bird IDs
##list stimuli played 
unique(data$song_played)
length(unique(data$song_played))
song_played<-unique(data$song_played)
write.csv(song_played, file="songs_played.csv", row.names=F)

#unique
#old way#list all the birds played, using the prefixes used in the stimuli list
#birds<-c('norm_bl111gr09', "FD_bl111gr09", "norm_bl21pu11", "FD_bl21pu11", "norm_dir", "norm_undir", "p183y24", "yelred_undir", "yelred_dir", "bl11p3", "g32b89", "fatmaleround", "oldmaleround", "bl4b13", 'bl43p196', 'bl36p46', 'o102p102', 'norm_bl111gr09', "FD_bl111gr09", "norm_bl21pu11", "FD_bl21pu11", "norm_undir", "p183y24", "yelred_undir", "yelred_dir", "bl11p3", "g32b89", "fatmaleround", "oldmaleround", 'blor', 'dir', 'undir', 'pu17pu18', 'blk17dir', 'blk17undir', 'pu21pu22', "norm_bl4b13", 'bl43p196', 'pu55bl8', 'bl4b13', 'directed_bl14y6', 'norm_bl14y6', 'FD_bl87bk3','norm_bl87bk3', 'FD_bl65w75', 'norm_bl65w75', 'FD_bl86pi11','norm_bl86pi11', 'FD_bl94pu34' , 'norm_bl94pu34', 'FD_bl100pu80', 'norm_bl100pu80', 'FD_bl33y35', 'norm_bl33y35', 'FD_bl58gr33', 'norm_bl58gr33',  'FD_bl87re02', 'norm_bl87re02', 'FD_bl43pi73', 'norm_bl43pi73', 'FD_bl63bk93', 'norm_bl63bk93', 'FD_bl90or19', 'norm_bl90or19', 'FD_bl71bl60', 'norm_bl71bl60', 'FD_bl44pi74', 'norm_bl44pi74',  'FD_bl74gy24', 'norm_bl74gy24', 'FD_bl61or11', 'norm_bl61or11', 'FD_bl31pi51', 'norm_bl31pi51', 'FD_bl49gy31', 'norm_bl49gy31', 'FD_bl80bk11', 'norm_bl80bk11', 'FD_bl62or12', 'norm_bl62or12', 'FD_bl84gr17', 'norm_bl84gr17','FD_bl87pu80', 'norm_bl87pu80')
#new way#column name cases must match
bird_played<- read.csv ("songsplayed_sorted_forcode.csv")
#for R, all data point needs a new row, and all info for that point should be in that row (repeated)
data <- merge (data, bird_played, "song_played") #reads the excel file that associates all stim for each bird with its unique name
write.csv(bird_played, file="birds_played.csv", row.names=F)
#below must be where things get mixed up and some rows get shifted one column to the right somehow?

#data$bird_played<-unlist(sapply(data$song_played, FUN=function(x){which(sapply(1:length(birds), FUN=function(y){grepl(birds[y],x)})==T)}))
#data$bird_played<-birds[data$bird_played]
unique(data$song_played)
unique(data$bird_played)

length(unique(data$date)) 
#groups data to show bird_ID, date, stimuli (bird) played, and how many times the female pulled for that song on that day
data_summary<-data%>%group_by(bird_ID, date, bird_played)%>%summarise_at('key_pecked', length)
#this breaks it down to show what key was pecked for what stim, and how many times, on a given day
data_summary_key<-data%>%group_by(bird_ID, date,bird_played,key_pecked)%>%summarise_at('time', length)
#removes first three string pulls (do I still need this?)
data_summary_key$time<-data_summary_key$time-3
#removes data where the they did not pull more than 3 times for a stim
data_summary_key<-subset(data_summary_key, time>0)
#creates a pass dataframe that shows the bird ID, date, and number of sessions within a test that they pulled (so 4 sessions = they pulled for each stim before and after the switch, beyond the threshold of 3 on each side)
pass<-data_summary_key%>%group_by(bird_ID, date)%>%summarise_at('key_pecked', length)
#displayed just the passed tests, by bird ID and date
notpass<-subset(pass, key_pecked<4)
pass<-subset(pass, key_pecked>=4)
#outputs the data summary key (this shows all the birds that pulled beyond 3 times threshold, may want to revise to show all tests to get a sense of test attempts)
write.csv(data_summary_key, file="data_summary_key.csv", row.names=F)
#outputs the passing birds list
write.csv(pass, file="passing_birds.csv", row.names=F)

#working with the passing data
data_pass<-subset(data,date%in%pass$date& bird_ID%in%pass$bird_ID)
data_notpass<-subset(data,date%in%notpass$date& bird_ID%in%notpass$bird_ID)
notpass_data_summary_key<-data_notpass%>%group_by(bird_ID, date,bird_played,key_pecked)%>%summarise_at('time', length)
notpass_data_summary<-data_notpass%>%group_by(bird_ID, date, bird_played)%>%summarise_at('key_pecked', length)
write.csv(notpass_data_summary_key, file="final_NOTpassing_birds_key.csv", row.names=F)
#loop over each bird_ID
#combine bird id and date in a new column
pass$bird_id_date<-paste(pass$bird_ID,pass$date, sep="_")
data_pass$bird_id_date<-paste(data_pass$bird_ID,data_pass$date, sep="_")
data_pass<-subset(data_pass, bird_id_date%in%pass$bird_id_date)
#make new column with combination of key and bird_played
data_pass$keys_and_songs<-paste(data_pass$key_pecked,data_pass$bird_played, sep="_")
#loop over bird_id_date column
#initialize an empty final_data<-tibble(colname=NA, colname2=0)
##final_data<-as_tibble(data.frame(matrix(NA,nrow=0,ncol=length(colnames(bid_rows)))))
##colnames(final_data) <-colnames(bid_rows)
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
##some of the switches need to be (switch+1) keep parantheses around
##check why some of the counts are 1 in final data from (switch1+1) to (switch2-1) and 4,5,6 
##summarize similiar to data_summary
final_data_summary<-final_data%>%group_by(bird_ID, date, bird_played)%>%summarise_at('key_pecked', length)
final_data_summary_key<-final_data%>%group_by(bird_ID, date,bird_played,key_pecked)%>%summarise_at('time', length)
final_data_summary_key<-subset(final_data_summary_key, time>0)
final_pass<-final_data_summary_key%>%group_by(bird_ID, date)%>%summarise_at('key_pecked', length)
final_pass<-subset(final_pass, key_pecked>=4)
write.csv(final_data_summary_key, file="final_data_summary_key.csv", row.names=F)
write.csv(final_pass, file="final_passing_birds.csv", row.names=F)
write.csv(final_data_summary, file="final_data_summary.csv", row.names=F)
