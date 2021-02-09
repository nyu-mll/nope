library(tidyverse)
library(stringr)

this.dir <- dirname(rstudioapi::getSourceEditorContext()$path)
setwd(this.dir)

dat = read.csv("../results/02_judgments/trials.csv")

stims = read.csv("../experiments/stimuli/all_annotations_cleaned.csv")
stims = stims %>% select(sent_id,trigger) %>% rename("id" = sent_id)

dat2 <- merge(dat,stims,by="id")

new_dat = NULL

ids<-unique(dat2$id)
types<-unique(dat2$type)

for(i in 1:length(ids)){
  for(j in 1:length(types)){
    temp<-dat2 %>%
      filter(id==ids[i],
             type==types[j])
    
    temp2<-temp%>%
      select(id,premise,hypothesis,type,trigger)
    temp2<-temp2[1,]
    
    temp2$resp_1 <- temp$response[1]
    temp2$resp_2 <- temp$response[2]
    temp2$resp_3 <- temp$response[3]
    temp2$resp_4 <- temp$response[4]
    temp2$resp_5 <- temp$response[5]
    temp2$mean_resp <- mean(temp$response)
    temp2$sd_resp <- sd(temp$response)
    
    new_dat = rbind(new_dat,temp2)
  }
}

write.csv(new_dat,"raw_responses.csv",row.names = F)
