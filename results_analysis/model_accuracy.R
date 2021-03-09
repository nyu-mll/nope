library(tidyverse)

this.dir <- dirname(rstudioapi::getSourceEditorContext()$path)
setwd(this.dir)

dat = read.csv("../model_results/02_judgments_preds_roberta_mnli.csv")

dat2<-dat%>%filter(trigger!='filler')

# overview of model results for each trigger and type
(plt<-ggplot(data=dat2, aes(x = type, fill=pred2))+
  geom_bar(stat='count')+
  facet_wrap(~trigger)+
  ggtitle("roberta large mnli")+
  theme(axis.text.x = element_text(angle = 45, vjust = 1, hjust=1),
        plot.title = element_text(hjust = 0.5)))

#----------------- assess model prediction as a function of human-rated probability --------------

C_resp = mean(dat2$mean_resp[dat2$pred2=="C"])
E_resp = mean(dat2$mean_resp[dat2$pred2=="E"])
N_resp = mean(dat2$mean_resp[dat2$pred2=="N"])

(plt2 <- ggplot(data=dat2, aes(x=trigger, y=mean_resp, col=pred2))+
   geom_jitter(alpha=0.5)+
   geom_hline(yintercept=C_resp, color="red")+
   geom_hline(yintercept=E_resp, color="darkgreen")+
   geom_hline(yintercept=N_resp, color="blue")+
   ggtitle("roberta large mnli by participant mean response")+
   theme(axis.text.x = element_text(angle = 45, vjust = 1, hjust=1),
         plot.title = element_text(hjust = 0.5)))

# dat3 <- dat2 %>%
#   mutate(diff = case_when(pred2=="C" ~ mean_resp - C_resp,
#                           pred2=="E" ~ mean_resp - E_resp,
#                           pred2=="N" ~ mean_resp - N_resp)) %>%
#   group_by(trigger, pred2) %>%
#   summarise(mean_diff = mean(diff), count=n())
# 
# (plt3 <- ggplot(data=dat3, aes(x=trigger, y = mean_diff, fill=pred2))+
#   geom_bar(stat="identity", position=position_dodge())+
#   ggtitle("roberta large mnli predictions difference from participant mean response")+
#   theme(axis.text.x = element_text(angle = 45, vjust = 1, hjust=1),
#           plot.title = element_text(hjust = 0.5)))

#---------------- calculate lexical overlap score for each item -----------------

dat3<-dat2
dat3$overlap = NA

for(i in 1:nrow(dat2)){
  s=dat2$premise[i]
  ss=unique(unlist(strsplit(gsub("\\.","",tolower(s))," ")))
  s2=dat2$hypothesis[i]
  ss2=unique(unlist(strsplit(gsub("\\.","",tolower(s2))," ")))
  o=intersect(ss,ss2)
  dat3$overlap[i]=(length(o)/length(ss2))*100
}

(plt3 = ggplot(dat3,aes(x=overlap,col=pred2))+
    geom_freqpoly(binwidth = 10,size=1.2)+
    #scale_y_continuous(trans = 'log10')+
    facet_grid(.~trigger)+
    xlim(c(0,100))+
    xlab("overlap rate")+
    ggtitle("Overlap rates in each protocol")+
    theme(plot.title = element_text(hjust = 0.5))
)
