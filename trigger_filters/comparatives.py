import spacy
from spacy import displacy
import numpy as np
import pandas as pd

coca1 = open("C:/Users/NYUCM Loaner Access/Documents/GitHub/presupposition_dataset/COCA_sample_10MB.txt")
comp_file = open("C:/Users/NYUCM Loaner Access/Documents/GitHub/presupposition_dataset/trigger_filters/outputs/comp.txt", "w")

#initialize spacy processor
nlp = spacy.load("en_core_web_sm")

# test sentences
comp_sent = "Clifford is a bigger dog than Cujo."  # should evaluate to true
comp_sent2 = "Clifford is a more giant dog than Cujo."  # should evaluate to true
non_comp_sent = "Clifford is a bigger dog than I thought,"  # should evaluate to false
other_comp = "Clifford is bigger of a dog than Cujo."  # should evaluate to true
other_comp2 = "Clifford is bigger a dog than Cujo."  # should evaluate to true, currently doesn't

# displacy.serve(nlp(other_comp2),style='dep')


def check_comparative(sentence):
    tokens = list(sentence)
    # tokens_str = [str(token) for token in tokens]
    adjs = []
    for token in tokens:  # check the sentence contains an adjective
        if token.pos_ == 'ADJ':
            if str(token.text) not in ["more", "most"]:
                adjs.append(token)
    for adj in adjs:  # get the noun the adj is modifying
        nouns = []
        # noun for 'Clifford is bigger of a dog than Cujo'
        for word in adj.children:
            if str(word.text) in ["of"]:
                for word2 in word.children:
                    if word2.dep_ == "pobj":
                        nouns.append(word2)
        # noun for 'Clifford is bigger a dog than Cujo' --> causes index error right now
        # if tokens_str.index(str(adj)) + 1 <= len(tokens_str):
        #     if tokens_str[tokens_str.index(str(adj)) + 1] in ["a", "an"]:
        #         det = tokens[tokens_str.index(str(adj)) + 1]
        #         for word3 in det.ancestors:
        #             if word3.dep_ == "attr":
        #                 nouns.append(word3)
        # noun for 'Clifford is a bigger dog than Cujo'
        for word in adj.ancestors:
            if word.dep_ == 'attr':
                nouns.append(word)
        for noun in nouns:  # check if the nouns have 'than' as a prepositional modifier
            for child in noun.children:
                if child.dep_ == 'prep' and str(child.text) == 'than':
                    return True
    return False


counter=0
for line in coca1:
    doc = nlp(line)
    context_buffer = ["", ""]
    for sentence in doc.sents:
        if check_comparative(sentence):
            counter += 1
            print(counter)
            comp_dict = {"context1": context_buffer[0], "context2": context_buffer[1], "sentence": sentence}
            comp_file.write(str(comp_dict) + "\n")
            comp_file.flush()
        context_buffer.pop(0)
        context_buffer.append(sentence)

comp_file.close()





#TODO: account for both 'Suzie is a richer woman than me' and 'Suzie is richer of a woman than me'
#TODO: get rid of cases like 'Suzie is a richer woman than I thought'
