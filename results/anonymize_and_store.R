library(tidyverse)
library(rjson)
library(jsonlite)

setwd("C:/Users/NYUCM Loaner Access/Documents/GitHub/presupposition_dataset/results")

anon_ids = read.csv("C:/Users/NYUCM Loaner Access/Documents/GitHub/SECRET/presup_dataset_SECRET/anon_id_links.csv")

SECRET_dir = "C:/Users/NYUCM Loaner Access/Documents/GitHub/SECRET/presup_dataset_SECRET/mturk_data/"
this_run = "01_prescreener_3"

read_json <- function(file){
  con <- file(file, open = "r")
  on.exit(close(con))
  jsonlite::stream_in(con, verbose = FALSE)
}

anonymize = function(dat,anons){
  dat2 = merge(dat,anons)
  dat3 = dat2 %>% select(-workerid)
  return(dat3)
}

dat<-read_json(paste0(SECRET_dir,this_run,".json"))

trials = dat[[1]][[1]]
subj_info = dat[[5]][[1]]

# create_ids
len_anons = nrow(anon_ids)
workerid = unique(trials$workerid)
anon_id = c((1+len_anons):(length(workerid)+len_anons))
updated_anons = cbind(workerid,anon_id)

full_anon_file = rbind(anon_ids,updated_anons)

write.csv(full_anon_file,"C:/Users/NYUCM Loaner Access/Documents/GitHub/SECRET/presup_dataset_SECRET/anon_id_links.csv", row.names=FALSE)

anon_trials = anonymize(trials,updated_anons)
anon_subj_info = anonymize(subj_info,updated_anons)

old_trials = read.csv("01_prescreener/trials.csv")
old_subj_info = read.csv("01_prescreener/subj_info.csv")

new_trials = rbind(old_trials,anon_trials)
new_subj_info = rbind(old_subj_info,anon_subj_info)

write.csv(new_trials,"01_prescreener/trials.csv", row.names=FALSE)
write.csv(new_subj_info,"01_prescreener/subj_info.csv", row.names=FALSE)
