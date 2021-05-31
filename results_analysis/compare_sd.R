library(tidyverse)

this.dir <- dirname(rstudioapi::getSourceEditorContext()$path)
setwd(this.dir)

set.seed(42)

trials = read.csv("../annotated_corpus/main_corpus.individual_ratings.csv",stringsAsFactors = F)

stims = read.csv("../experiments/stimuli/all_annotations_cleaned.csv")
stims = stims %>% select(sent_id,trigger) %>% rename("id" = sent_id)

# separate out info about which items are adversarial
trials_sep <- trials %>%
  separate(id, c("id_num","adv"), sep = "_")%>%
  mutate(adversarial = case_when(is.na(adv) ~ "non",
                                 !is.na(adv) ~ "adv"))%>%
  mutate(id = case_when(adversarial=="non" ~ id_num,
                        adversarial=="adv" ~ adv))%>%
  select(-adv,-id_num,-X)

# add in trigger info
trials2 <- merge(trials_sep,stims,by="id")

trials3 <- trials2 %>%
  group_by(id, type, trigger, adversarial)%>%
  summarise(mean_resp = mean(response),
            stdev = sd(response))

t3_nonadv <- filter(trials3, adversarial == "non")

(plt<-ggplot(data=t3_nonadv, aes(x=type, y=stdev, col=type, fill=type))+
    #geom_boxplot(position=position_dodge(0.7),alpha=0.1, width=0.5, lwd=2)+
    geom_violin(position=position_dodge(),alpha=0.8)+
    #geom_jitter(width=0.1,height=0,alpha=0.2,size=2)+
    ggtitle("Comparison of standard deviation of response across triggers")+
    theme(plot.title = element_text(hjust = 0.5),
          axis.text.x = element_blank(),
          legend.position = c(0.85, 0.2))+
          #axis.text.x = element_text(angle = 20, vjust = 1, hjust=1))+
    xlab("Trigger & context condition")+
    ylab("Standard deviation of responses")+
    facet_wrap(~trigger))

ggsave("figures/stdev_comparison.png",plt,width=6.5,height=5)
