library(tidyverse)
library(rjson)
library(jsonlite)

setwd("C:/Users/NYUCM Loaner Access/Documents/GitHub/presupposition_dataset/results")

anon_ids = read.csv("C:/Users/NYUCM Loaner Access/Documents/GitHub/SECRET/presup_dataset_SECRET/anon_id_links.csv")

SECRET_dir = "C:/Users/NYUCM Loaner Access/Documents/GitHub/SECRET/presup_dataset_SECRET/mturk_data/"
this_run = "01_prescreener"

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

write.csv(updated_anons,"C:/Users/NYUCM Loaner Access/Documents/GitHub/SECRET/presup_dataset_SECRET/anon_id_links.csv")

anon_trials = anonymize(trials,updated_anons)
anon_subj_info = anonymize(subj_info,updated_anons)

write.csv(anon_trials,paste0(this_run,"/","trials.csv"))
write.csv(anon_subj_info,paste0(this_run,"/","subj_info.csv"))
