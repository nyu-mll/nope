library(tidyr)
library(dplyr)
library(stringr)

setwd("C:/Users/NYUCM Loaner Access/Documents/GitHub/presupposition_dataset/annotations")

full_files = list.files("full",pattern='*.csv')
new_annot_files = list.files("iaa_check",pattern='*.csv')

dat = NULL
for(i in 1:length(full_files)){
  tmp = read.csv(paste0("full/",full_files[i]))
  if("X" %in% colnames(tmp)){tmp = select(tmp, -X)}
  tmp$annotator = str_match(full_files[i], "- \\s*(.*?)\\s*.csv")[,2]
  tmp$original = "Yes"
  dat = rbind(dat,tmp)
  
  tmp2 = read.csv(paste0("iaa_check/",new_annot_files[i]))
  if("X" %in% colnames(tmp2)){tmp2 = select(tmp2, -X)}
  tmp2$annotator = str_match(full_files[i], "- \\s*(.*?)\\s*.csv")[,2]
  tmp2$original = "No"
  dat = rbind(dat,tmp2)
}

check_ids = unique(dat$sent_id[dat$original=="No"])

dat2<-dat%>%
  filter(sent_id %in% check_ids)%>%
  filter(!is.na(appropriate.))

# check equivalency of metadata info
dat3 <- dat2 %>%
  replace(is.na(.), "")%>%
  select(-notes,-context1_speaker,-context1,-context2_speaker,-context2,-trigger_data,-speaker)%>%
  gather("Question","Response",-trigger,-sentence,-presupposition,-negated_sentence,-altered.sentence,-sent_id,-annotator,-original)%>%
  group_by(sent_id,Question)%>%
  mutate(count=n())%>%
  ungroup()%>%
  group_by(sent_id,Question)%>%
  summarise(yes_rate=sum(Response=="Y")/mean(count))%>%
  mutate(agree_rate = ifelse(yes_rate == 1, 1,
                             ifelse(yes_rate == 0, 1, 0)))%>%
  group_by(Question)%>%
  summarise(agreement = mean(agree_rate))

dat4 = NULL
for(i in 1:length(check_ids)){
  temp = dat2 %>%
    select(sent_id,annotator,original,sentence,altered.sentence,appropriate.,negatable.,negated_sentence,presupposition)
  temp2 = temp %>%
    filter(sent_id == check_ids[i])
  original = filter(temp2, original=="Yes")
  non_original = temp2 %>%
    filter(original == "No")%>%
    select(-sent_id,-original,-sentence)
  non_original_1 = non_original[1,]
  colnames(non_original_1) <- paste(colnames(non_original_1), "1", sep = "_")
  if(nrow(non_original)==2){
    non_original_2 = non_original[2,]
    colnames(non_original_2) <- paste(colnames(non_original_2), "2", sep = "_")
  }
  if(nrow(non_original)==1){
    non_original_2 = data.frame(matrix(NA, nrow = 1, ncol = ncol(non_original)))
    colnames(non_original_2) <- paste(colnames(non_original), "2", sep = "_")
  }
  temp_dat = cbind(original,non_original_1,non_original_2)
  dat4 = rbind(dat4,temp_dat)
}

dat5 <- dat4 %>%
  select(-original)%>%
  mutate(agree_appropriate = ifelse(appropriate.==appropriate._1 & !is.na(appropriate._2) & appropriate. == appropriate._2, 1, 
                                    ifelse(appropriate.==appropriate._1 & is.na(appropriate._2), 1, 0))) %>%
  mutate(agree_negatable = ifelse(negatable.==negatable._1 & !is.na(negatable._2) & negatable. == negatable._2, 1, 
                                    ifelse(negatable.==negatable._1 & is.na(negatable._2), 1, 0)))

write.csv(dat5,"manual_checks.csv")
