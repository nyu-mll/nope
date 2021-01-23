library(tidyverse)

setwd("C:/Users/NYUCM Loaner Access/Documents/GitHub/presupposition_dataset/results")

dat = read.csv("01_prescreener/trials.csv")

remove_practice = c("practice_1","practice_2","practice_3")

dat2 <- dat %>%
  select(-premise,-hypothesis,-trial,-Answer.time_in_minutes)%>%
  filter(!id %in% remove_practice)%>%
  mutate(response2 = as.numeric(as.character(response)))



plt <- ggplot(data = dat2, aes(x = id, y = response2))+
  geom_jitter(width=0.2,height=0,alpha=0.6,size=2)+
  geom_boxplot(position=position_dodge(),alpha=0)+
  ggtitle(paste0("Prescreener, n = ",length(unique(dat2$anon_id))))+
  theme(plot.title = element_text(hjust = 0.5))+
  xlab("Context condition")+
  ylab("Response")
plt
