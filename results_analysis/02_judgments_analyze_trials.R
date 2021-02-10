library(tidyverse)
library(stringr)

this.dir <- dirname(rstudioapi::getSourceEditorContext()$path)
setwd(this.dir)

dat = read.csv("../results/02_judgments/trials.csv")

stims = read.csv("../experiments/stimuli/all_annotations_cleaned.csv")
stims = stims %>% select(sent_id,trigger) %>% rename("id" = sent_id)

# ----------------- LOOK AT THE FILLER ITEMS -----------------

dat2 <- dat %>%
  filter(type=="filler")%>%
  mutate(expected_resp = case_when(str_detect(id, "e_filler") ~ "entailment",
                                   str_detect(id, "c_filler") ~ "contradiction"))

# PLOT ANNOTATOR ACCURACY
(plt = ggplot(data=dat2, aes(x=as.factor(anon_id),y=response,col=expected_resp))+
    geom_jitter())

# CALCULATE ANNOTATOR ACCURACY
dat2_corr <- dat2 %>%
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
            count = n()/5)

# PLOT RESPONSES ON EACH FILLER ITEM
(plt.fill <- ggplot(data=dat2, aes(x=as.factor(id),y=response))+
     geom_jitter(alpha=0.3,size=2)+
     geom_boxplot(alpha=0)+
     theme(axis.text.x=element_blank(),
           axis.ticks.x=element_blank())+
     facet_wrap(~expected_resp,scales="free_x"))


# ----------------- LOOK AT THE TARGET ITEMS -----------------

# PLOT ALL CONDITIONS WITH SCATTERPLOTS AND BOXPLOTS
dat3 <- dat %>%
  filter(type!="filler")%>%
  group_by(id,type)%>%
  summarise(mean_resp = mean(response))
  
dat4 <- merge(dat3,stims,by="id")

plt2 = ggplot(data=dat4, aes(x=type,y=mean_resp,col=type))+
  geom_jitter()+
  geom_boxplot(alpha=0)+
  facet_wrap(~trigger)+
  ggtitle("Judgments pilot, full data with 150 responses")+
  theme(plot.title = element_text(hjust = 0.5),
        axis.title.x=element_blank(),
        axis.text.x=element_blank(),
        axis.ticks.x=element_blank(),
        legend.position = c(0.9, 0.2))
plt2

# MAKE LINE PLOTS SHOWING PRIOR TO POSTERIOR
dat5<-dat4%>%
  spread(type,mean_resp)%>%
  gather(condition,posterior,-id,-trigger,-`target-prior`)%>%
  rename("prior"=`target-prior`)%>%
  gather(rating_type,response,-id,-trigger,-condition)

dat5$rating_type <- factor(dat5$rating_type, levels = c("prior","posterior"))
dat5$condition <- factor(dat5$condition, levels = c("target-original","target-negated"))
(plt3 <- ggplot(data=dat5,aes(x=rating_type,y=response,group=id))+
  geom_line()+
  facet_grid(condition~trigger)+
  scale_x_discrete(expand=c(0,0.05))+
  ggtitle("Judgments pilot, full data with 150 responses (lines show prior to posterior judgment)")+
  theme(plot.title = element_text(hjust = 0.5),
        axis.title.x=element_blank(),
        axis.text.x=element_blank(),
        axis.ticks.x=element_blank())
)
  
