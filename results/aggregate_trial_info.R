library(tidyverse)

this.dir <- dirname(rstudioapi::getSourceEditorContext()$path)
setwd(this.dir)


dat = read.csv("./01_prescreener/trials.csv")

remove_practice = c("practice_1","practice_2","practice_3")

dat2 <- dat %>%
  select(-premise,-hypothesis,-Answer.time_in_minutes)%>%
  filter(!id %in% remove_practice)%>%
  mutate(response2 = as.numeric(as.character(response)))

expected_values = data.frame(id = c("screener_1","screener_2","screener_3","screener_4","screener_5",
                                    "screener_6","screener_7","screener_8","screener_9","screener_10"),
                             expected_high = c(.999,1,.01,.1,1,.2,.6,.9,.35,0)*100,
                             expected_low = c(.5,   1,  0, 0,1, 0,.4,.1,.25,0)*100)
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

dat3 %>% ggplot(aes(x=id, y=response2)) +
  geom_point() +
  facet_wrap(~anon_id) +
  geom_errorbar(aes(ymin=expected_low, ymax=expected_high), col="red", size=.4)

dat3 = dat3 %>% mutate(dev = if_else(response2 >= expected_low & response2 <= expected_high, 0, if_else(response2 < expected_low, response2-expected_low, response2-expected_high)))

dat3 %>% ggplot(aes(x=(gsub("screener_", "", id)), y=dev)) +
  geom_hline(yintercept=0, col="red") +
  geom_point() +
  facet_wrap(~anon_id) +
  ylim(-20,20) +
  xlab("Context condition")+
  ylab("Deviation from expected response")

dat3 %>% ggplot(aes(x=trial, y=dev, col=id)) +
  geom_hline(yintercept=0, col="red") +
  geom_point() +
  facet_wrap(~anon_id) +
  ylim(-20,20) +
  xlab("Context condition")+
  ylab("Deviation from expected response")


dat3 %>% filter(dev == 0) %>% ggplot(aes(x=dev)) + geom_histogram(binwidth = 1) + facet_wrap(~anon_id) 

within_range = dat3 %>% filter(dev == 0) %>% group_by(anon_id) %>% dplyr::summarize(count = n()) %>% arrange(count)

within_range %>% 
  ggplot(aes(x=count)) +  scale_x_continuous(">= exactly correct", 1:10, waiver(), limits=c(0.1,10.5)) + ylab("number of participants") +
  stat_bin(aes(y=rev(cumsum(rev(..count..))), label=rev(cumsum(rev(..count..)))), binwidth=1, geom="text", vjust=-.5) +
  stat_bin(aes(y=rev(cumsum(rev(..count..)))), binwidth=1)


within_range2 = dat3 %>% filter(abs(dev) < 5) %>% group_by(anon_id) %>% dplyr::summarize(count = n()) %>% arrange(count)


within_range2 %>% 
  ggplot(aes(x=count)) +  scale_x_continuous(">= mostly correct (+/- 5%)", 1:10, waiver(), limits=c(0.1,10.5)) + ylab("number of participants") +
  stat_bin(aes(y=rev(cumsum(rev(..count..))), label=rev(cumsum(rev(..count..)))), binwidth=1, geom="text", vjust=-.5) +
  stat_bin(aes(y=rev(cumsum(rev(..count..)))), binwidth=1)


for(value in unique(expected_values$id)){
  plt = plt+annotate("pointrange", x = value, y = expected_values$mean[expected_values$id==value], 
           ymin = expected_values$expected_low[expected_values$id==value], ymax = expected_values$expected_high[expected_values$id==value],
           colour = "red", size = 1.5, alpha = 0.5)
}

plt
