library(tidyverse)

setwd("C:/Users/NYUCM Loaner Access/Documents/GitHub/presupposition_dataset/results")

dat = read.csv("01_prescreener/trials.csv")

remove_practice = c("practice_1","practice_2","practice_3")

dat2 <- dat %>%
  select(-premise,-hypothesis,-trial)%>%
  filter(!id %in% remove_practice)%>%
  mutate(response2 = as.numeric(as.character(response)))

times <- dat2 %>%
  filter(Answer.time_in_minutes < 40)%>%
  filter(Answer.time_in_minutes > 4)%>%
  group_by(anon_id)%>%
  summarise(time = mean(Answer.time_in_minutes))%>%
  mutate(in_range_1sd = case_when(time > mean(time)+sd(time) | time < mean(time)-sd(time) ~ 0,
                                  time < mean(time)+sd(time) & time > mean(time)-sd(time) ~ 1,
                                  ))

to_remove = c()
flag = T

clean_dat = dat2

# iteratively remove participants who are >2 sd outside of range on 3+ items
while(flag == T){
  clean_dat = clean_dat %>%
    filter(!anon_id %in% to_remove)%>%
    #filter(Answer.time_in_minutes > 4)%>% # just assume no one actually did this in under 4 min
    group_by(id)%>%
    #mutate(mean_rating = mean(response2),
    #          sd_rating = sd(response2))%>%
    #ungroup()%>%
    mutate(in_range_1sd = case_when(response2 > mean(response2)+sd(response2) | response2 < mean(response2)-sd(response2) ~ 0,
                                    response2 < mean(response2)+sd(response2) & response2 > mean(response2)-sd(response2) ~ 1,
    ))%>%
    mutate(in_range_2sd = case_when(response2 > mean(response2)+2*sd(response2) | response2 < mean(response2)-2*sd(response2) ~ 0,
                                    response2 < mean(response2)+2*sd(response2) & response2 > mean(response2)-2*sd(response2) ~ 1,
    ))%>%
    ungroup()%>%
    group_by(anon_id)%>%
    mutate(score = mean(in_range_2sd))
  new_remove = unique(clean_dat$anon_id[clean_dat$score < 0.8])
  if(length(new_remove)>0){
    print("removing:")
    print(new_remove)
    print("")
    to_remove = c(to_remove,new_remove)
  } else {
    flag = F
  }
}

print(to_remove)

table(clean_dat$in_range_2sd,clean_dat$id)


  