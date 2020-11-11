import spacy
from pragmatics_dataset.trigger_filters.spacy_utils import get_dependents_string
import re
import numpy as np
from pragmatics_dataset.negated_nli.negate_sentences import negate_main_verb

factives = [l.strip() for l in open("wordlists/factives.jsonl")]

file = open("../COCA_sample_10MB.txt")
output = open("outputs/factives.jsonl", "w")

nlp = spacy.load("en_core_web_sm")

context_buffer = ["", ""]

def check_sentence_for_factives(sentence):
    factives_in_sentence = [t for t in sentence if t.lemma_ in factives]
    if len(factives_in_sentence) > 0:
        for factive_verb in factives_in_sentence:
            comp_children = [c for c in factive_verb.children if c.dep_ == "ccomp"]
            if len(comp_children) > 0:
                comp_clause = get_dependents_string(comp_children[0])
                return True, factive_verb, comp_clause
    return False, None, None


def check_sentence_for_quote(sentence, factive_verb, comp_clause):
    pass


for line in file:
    doc = nlp(line)
    for sentence in doc.sents:
        contains_factive, factive_verb, comp_clause = check_sentence_for_factives(sentence)
        if contains_factive:
            example = {
                "sentence": sentence.text.strip(),
                "context1": context_buffer[0].strip(),
                "context2": context_buffer[1].strip(),
                "factive": factive_verb.text,
                "embedded_clause": comp_clause
            }
            output.write(str(example) + "\n")
            output.flush()
        context_buffer.pop(0)
        context_buffer.append(sentence.text)