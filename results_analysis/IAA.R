library(irr)
library(tidyverse)

this.dir <- dirname(rstudioapi::getSourceEditorContext()$path)
setwd(this.dir)

trials = read.csv("../results/02_judgments/trials.csv")

stims = read.csv("../experiments/stimuli/all_annotations_cleaned.csv")
stims = stims %>% select(sent_id,trigger) %>% rename("id" = sent_id)

trials2 <- merge(trials,stims,by="id")

triggers = unique(trials2$trigger)
types = unique(trials2$type)

data = data.frame(matrix(ncol = length(types), nrow = length(triggers)))
colnames(data) = types
rownames(data) = triggers

for(tr in triggers){
  for(ty in types){
    trials3<-trials2 %>%
      filter(type == ty)%>%
      filter(trigger == tr) %>%
      select(id,response,anon_id)%>%
      spread(id,response)
    t3<- data.matrix(trials3)
    k=kripp.alpha(t3,"interval")
    data[as.character(tr),as.character(ty)] <- k$value
  }
}

View(data)
