library(tidyverse)
library(stringr)

this.dir <- dirname(rstudioapi::getSourceEditorContext()$path)
setwd(this.dir)

dat = read.csv("../results/02_judgments/trials.csv")

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
  geom_boxplot(alpha=0)+
  facet_wrap(~trigger)+
  ggtitle("Judgments pilot, partial data with 104 responses")+
  theme(plot.title = element_text(hjust = 0.5),
        axis.title.x=element_blank(),
        axis.text.x=element_blank(),
        axis.ticks.x=element_blank(),
        legend.position = c(0.9, 0.2))
plt2
  
