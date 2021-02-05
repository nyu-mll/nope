library(tidyverse)
library(stringr)

this.dir <- dirname(rstudioapi::getSourceEditorContext()$path)
setwd(this.dir)

dat = read.csv("./02_judgments/trials.csv")

stims = read.csv("../experiments/stimuli/all_annotations_cleaned.csv")
stims = stims %>% select(sent_id,trigger) %>% rename("id" = sent_id)

###################################
# LOOK AT THE FILLER ITEMS

dat2 <- dat %>%
  filter(type=="filler")%>%
  mutate(expected_resp = case_when(str_detect(id, "e_filler") ~ "entailment",
                                   str_detect(id, "c_filler") ~ "contradiction"))

(plt = ggplot(data=dat2, aes(x=as.factor(anon_id),y=response,col=expected_resp))+
    geom_jitter())

###################################
# LOOK AT THE TARGET ITEMS

dat3 <- dat %>%
  filter(type!="filler")%>%
  group_by(id,type)%>%
  summarise(mean_resp = mean(response))
  
dat4 <- merge(dat3,stims,by="id")

plt2 = ggplot(data=dat4, aes(x=type,y=mean_resp,col=type))+
  geom_jitter()+
  geom_boxplot(alpha=0.1)+
  facet_wrap(~trigger)+
  theme(axis.text.x = element_text(angle = 45, vjust = 1, hjust=1))+
  ggtitle("Judgments pilot, partial data with 11 responses")+
  theme(plot.title = element_text(hjust = 0.5))
plt2
  
