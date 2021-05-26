library(irr)
library(tidyverse)

this.dir <- dirname(rstudioapi::getSourceEditorContext()$path)
setwd(this.dir)

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
  select(-adv,-id_num)

# add in trigger info
trials2 <- merge(trials_sep,stims,by="id")

# which items are adversarial
trials2 <- trials2 %>% unite("trigger",trigger,adversarial, sep="_")

# ---------------------------------------------------
# loop through and get alpha values for each trigger & type

triggers = unique(trials2$trigger)
types = unique(trials2$type)

data = data.frame(matrix(ncol = length(types), nrow = length(triggers)))
colnames(data) = types
rownames(data) = triggers

# can get rid of later, but right now can't run these because of duplicated values
cant_run = c("embedded_question_non","implicative_predicates_non","implicative_predicates_non",
             "re_verbs_non","temporal_adverbs_adv","clefts_non")
triggers = triggers[!triggers %in% cant_run]

for(tr in triggers){
  for(ty in types){
    trials3<-trials2 %>%
      filter(type == ty)%>%
      filter(trigger == tr) %>%
      select(id,response,anon_id)%>%
      spread(id,response)
    t3<- data.matrix(trials3)
    k=kripp.alpha(t3,"interval")
    data[as.character(tr),as.character(ty)] <- k$value
  }
}

View(data)


# ---------------------------------------------------
# bootstrapping for distribution & CIs









# ---------- LOOK AT ALPHA FOR FILLER ITEMS ---------- 
fillers <- trials %>% 
  filter(type == "filler") %>%
  mutate(expected_resp = case_when(str_detect(id, "e_filler") ~ "entailment",
                                   str_detect(id, "c_filler") ~ "contradiction"))

for(ty in unique(fillers$expected_resp)){
  fillers2<-fillers %>%
    filter(expected_resp == ty)%>%
    select(id,response,anon_id)%>%
    spread(id,response)
  f2<- data.matrix(fillers2)
  k=kripp.alpha(f2,"interval")
  print(ty)
  print(k)
}


# ----------GET OVERALL VALUES ---------- 
for(ty in unique(trials$type)){
  trials5<-trials %>%
    filter(type == ty)%>%
    select(id,response,anon_id)%>%
    spread(id,response)
  t5<- data.matrix(trials5)
  k=kripp.alpha(t5,"interval")
  print(ty)
  print(k)
}


# ---------- OVERALL OVERALL ---------- 
trials6 <- trials %>%
  unite('ids',c(id,type))%>%
  select(ids,response,anon_id)%>%
  spread(ids,response)
t6<- data.matrix(trials6)
kripp.alpha(t6,"interval")
