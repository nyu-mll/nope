library(tidyverse)

setwd("C:/Users/NYUCM Loaner Access/Documents/GitHub/presupposition_dataset/results")

dat = read.csv("01_prescreener/subj_info.csv")

dat2 = dat %>%
  gather("Question","Value", -anon_id)

plot_values = c("enjoyment", "asses", "fairprice")
dat3 <- dat2 %>% 
  filter(Question %in% plot_values) %>%
  filter(Value != -1)

plt = ggplot(data=dat3, aes(x=Value))+
  geom_bar(stat = 'count')+
  facet_wrap(~Question,scales = "free_x")
plt
