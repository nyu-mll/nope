library(tidyverse)
library(stringr)

this.dir <- dirname(rstudioapi::getSourceEditorContext()$path)
setwd(this.dir)

dat = read.csv("../results/04_judgments_part2/trials.csv")

stims = read.csv("../experiments/stimuli/all_annotations_cleaned.csv")
stims = stims %>% select(sent_id,trigger) %>% rename("id" = sent_id)

# ----------------- LOOK AT THE FILLER ITEMS FOR 03_JUDGMENT_REANNOTATIONS -----------------

dat2 <- dat %>%
  filter(type=="filler")%>%
  mutate(expected_resp = case_when(str_detect(id, "e_filler") ~ "entailment",
                                   str_detect(id, "c_filler") ~ "contradiction",
                                   str_detect(id, 'n_filler') ~ "neutral"))

low = c(26, 52)
dat2 <- dat2 %>% filter(anon_id %in% low)

# PLOT ANNOTATOR ACCURACY
(plt = ggplot(data=dat2, aes(x=as.factor(anon_id),y=response,col=expected_resp))+
    geom_jitter())

# CALCULATE ANNOTATOR ACCURACY
dat_corr <- dat2 %>%
  filter(expected_resp != "neutral") %>%
  mutate(corr_strong = case_when(expected_resp == "entailment" & response >= 99 ~ 1,
                                 expected_resp == "entailment" & response < 99 ~ 0,
                                 expected_resp == "contradiction" & response <= 1 ~ 1,
                                 expected_resp == "contradiction" & response > 1 ~ 0))%>%
  mutate(corr_weak = case_when(expected_resp == "entailment" & response >= 90 ~ 1,
                               expected_resp == "entailment" & response < 90 ~ 0,
                               expected_resp == "contradiction" & response <= 10 ~ 1,
                               expected_resp == "contradiction" & response > 10 ~ 0))%>%
  group_by(anon_id) %>%
  summarise(mean_corr_strong = mean(corr_strong),
            mean_corr_weak = mean(corr_weak),
            count = n())

# PLOT RESPONSES ON EACH FILLER ITEM
(plt.fill <- ggplot(data=dat2, aes(x=as.factor(id),y=response))+
    geom_jitter(alpha=0.3,size=2)+
    geom_boxplot(alpha=0)+
    theme(axis.text.x=element_blank(),
          axis.ticks.x=element_blank())+
    facet_wrap(~expected_resp,scales="free_x"))


# ----------------- LOOK AT THE TARGET ITEMS -----------------

# PLOT ALL CONDITIONS WITH SCATTERPLOTS AND BOXPLOTS
dat_a <- dat %>%
  filter(type!="filler")%>%
  group_by(id,type)%>%
  summarise(mean_resp = mean(response))

dat_b <- merge(dat_a,stims,by="id")

plt2 = ggplot(data=dat_b, aes(x=type,y=mean_resp,col=type))+
  geom_jitter()+
  geom_boxplot(alpha=0)+
  ggtitle(" ")+
  facet_wrap(~trigger)+
  theme(plot.title = element_text(hjust = 0.5),
        axis.title.x=element_blank(),
        axis.text.x=element_blank(),
        axis.ticks.x=element_blank(),
        legend.position = c(0.85, 0.2))
plt2


