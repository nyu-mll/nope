import spacy
from trigger_filters.spacy_utils import get_dependents_string

import en_core_web_sm
import numpy as np

infile = open('C:/Users/meinp/Documents/GitHub/presupposition_dataset/COCA_sample_10MB.txt', 'r')
outfile = open('C:/Users/meinp/Documents/GitHub/presupposition_dataset/trigger_filters/outputs/temporal_adverbs_no_gerunds.jsonl', 'w')

temporal_prepositions = ['before', 'after', 'while', 'since', 'because']
accepted_head_tags = {
    # 'VBG': 'gerund',
    'VBN': 'past-participle',
    'VBD': 'past',
    'VBP': 'non-3sg-present',
    'VBZ': '3sg-present',
    'VB': 'base',
}

#TODO: filter by both POS and syntax

# initialize spacy processor
nlp = spacy.load('en_core_web_sm')

context_buffer = ['', '']

# optional: take first n
counter = 0
n = 500

for line in infile:
    # counter += 1
    # if counter > 500:
    #     break
    doc = nlp(line)
    for sentence in doc.sents:
        preps_in_sentence = [word for word in sentence if word.lemma_ in temporal_prepositions]
        if len(preps_in_sentence) > 0:
            for prep in preps_in_sentence:
                # collect the immediate children
                prep_children = [child for child in prep.children]
                # get the tag(s) of the immediate child
                prep_tags = [child.tag_ for child in prep_children]
                accepted_prep_tags = list(set(prep_tags) & set(accepted_head_tags.keys()))
                if len(prep_children) > 0 and len(accepted_prep_tags) > 0:
                    temporal_pp = get_dependents_string(prep_children[0])
                    # print(temporal_pp)
                    example = {
                        "preposition": prep.text,
                        "head_tag": prep_tags,
                        "embedded_clause": temporal_pp,
                        "sentence": sentence.text.strip(),
                        "context1": context_buffer[0].strip(),
                        "context2": context_buffer[1].strip(),
                    }
                    outfile.write(str(example) + "\n")
                    outfile.flush()

        context_buffer.pop(0)
        context_buffer.append(sentence.text)

infile.close()
outfile.close()
