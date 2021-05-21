library(tidyverse)
library(stringr)

this.dir <- dirname(rstudioapi::getSourceEditorContext()$path)
setwd(this.dir)


# load pilot judgements
dat_pilot = read.csv("../results/02_judgments/trials.csv")

dat_pilot.target = dat_pilot %>% filter(type != "filler")
dat_pilot.fillers = dat_pilot %>% filter(type == "filler")

dat_pilot.target_n = nrow(dat_pilot.target)

dat_pilot_reannotations = read.csv("../results/03_judgment_reannotations/trials.csv")
dat_pilot_reannotations.target = dat_pilot_reannotations %>% filter(type != "filler")
dat_pilot_reannotations.fillers = dat_pilot_reannotations %>% filter(type == "filler")


reannotation_ids = unique(dat_pilot_reannotations.target$id)

#discard re-annotated data from dat_pilot

dat_pilot.target = dat_pilot.target %>% filter(!(id %in% reannotation_ids))
dat_pilot.target = rbind(dat_pilot.target, dat_pilot_reannotations.target)

print("Original number of pilot examples:")
print(dat_pilot.target_n)

print("After merging with re-annotation examples:")
print(nrow(dat_pilot.target))


# load original annotation data

dat_main = read.csv("../results/04_judgments_part2/trials.csv")
dat_main.target = dat_main %>% filter(type != "filler")
dat_main.fillers = dat_main %>% filter(type == "filler")

dat_main.target_n = nrow(dat_main.target)
dat_main.target_n_items = dat_main.target %>% group_by(id, type) %>% dplyr::summarize(n = n()) %>% nrow()

# compute accuracy for each worker on fillers

dat_main.fillers = dat_main.fillers %>% 
  mutate(expected_resp = case_when(str_detect(id, "e_filler") ~ "entailment",
                                   str_detect(id, "c_filler") ~ "contradiction",
                                   str_detect(id, 'n_filler') ~ "neutral"))

dat_main.corr <- dat_main.fillers %>%
  filter(expected_resp != "neutral") %>%
  mutate(corr_weak = case_when(expected_resp == "entailment" & response >= 90 ~ 1,
                               expected_resp == "entailment" & response < 90 ~ 0,
                               expected_resp == "contradiction" & response <= 10 ~ 1,
                               expected_resp == "contradiction" & response > 10 ~ 0))%>%
  group_by(anon_id) %>%
  summarise(mean_corr_weak = mean(corr_weak),
            count = n())

dat_main.low_acc = dat_main.corr %>% filter(mean_corr_weak < .7) %>% .$anon_id

dat_main.target = dat_main.target %>% filter(!(anon_id %in% dat_main.low_acc))

# load items that had to be re-annotated
reannotation_list = read.csv("../experiments/_reannotation_assignments/reannotations_after_04.csv")
reannotation_list.complete_reannotation_ids = reannotation_list %>% 
  mutate(full_id = paste(id, type, sep="-")) %>% 
  filter(reason != "low_acc_worker_removed") %>% 
  .$full_id

dat_pilot.target = dat_pilot.target %>% 
  mutate(full_id = paste(id, type, sep="-")) %>%
  filter(!(full_id %in% reannotation_list.complete_reannotation_ids)) %>%
  dplyr::select(-full_id)

dat_main.target = dat_main.target %>% 
  mutate(full_id = paste(id, type, sep="-")) %>%
  filter(!(full_id %in% reannotation_list.complete_reannotation_ids)) %>%
  dplyr::select(-full_id)


# load reannotation data

dat_main_reannotations = read.csv("../results/05_judgment_reannotations/trials.csv")
dat_main_reannotations.target = dat_main_reannotations %>% filter(type != "filler")
dat_main_reannotations.fillers = dat_main_reannotations %>% filter(type == "filler")

dat_all.target = rbind(dat_pilot.target, dat_main.target, dat_main_reannotations.target)

# remove one annotation from 2 items that were accidentally annotated 6 times
dat_all.target = dat_all.target %>% 
  filter(!(anon_id == 144 & id == 2004)) %>%
  filter(!(anon_id == 104 & id == "adv_364"))
  

print("Original number of examples:")
print(dat_main.target_n + dat_pilot.target_n)

print("After merging with re-annotation examples:")
print(nrow(dat_all.target))

dat_all.target_no_prior = dat_all.target %>% filter(type != "target-prior")
dat_all.target_prior = dat_all.target %>% filter(type == "target-prior")


write.csv(dat_all.target_no_prior, file="../annotated_corpus/main_corpus.individual_ratings.csv")
write.csv(dat_all.target_prior, file="../annotated_corpus/priors.individual_ratings.csv")
