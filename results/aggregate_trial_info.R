library(tidyverse)

setwd("C:/Users/NYUCM Loaner Access/Documents/GitHub/presupposition_dataset/results")

dat = read.csv("01_prescreener/trials.csv")

remove_practice = c("practice_1","practice_2","practice_3")

dat2 <- dat %>%
  select(-premise,-hypothesis,-trial,-Answer.time_in_minutes)%>%
  filter(!id %in% remove_practice)%>%
  mutate(response2 = as.numeric(as.character(response)))

expected_values = data.frame(id = c("screener_1","screener_2","screener_3","screener_4","screener_5",
                                    "screener_6","screener_7","screener_8","screener_9","screener_10"),
                             expected_high = c(1,1,.01,.1,1,.2,.6,.9,.35,0)*100,
                             expected_low = c(.8,1,0,0,1,0,.4,.1,.25,0)*100)
expected_values = expected_values %>%
  mutate(mean = (expected_high+expected_low)/2)

dat3 = merge(dat2,expected_values)

plt <- ggplot(data = dat3, aes(x = id, y = response2))+
  geom_jitter(width=0.2,height=0,alpha=0.6,size=2)+
  geom_boxplot(position=position_dodge(),alpha=0)+
  ggtitle(paste0("Prescreener, n = ",length(unique(dat2$anon_id))))+
  theme(plot.title = element_text(hjust = 0.5))+
  xlab("Context condition")+
  ylab("Response")

for(value in unique(expected_values$id)){
  plt = plt+annotate("pointrange", x = value, y = expected_values$mean[expected_values$id==value], 
           ymin = expected_values$expected_low[expected_values$id==value], ymax = expected_values$expected_high[expected_values$id==value],
           colour = "red", size = 1.5, alpha = 0.5)
}

plt
