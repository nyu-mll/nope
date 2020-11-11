import spacy
import json
import numpy as np
from spacy import displacy

implicative_phrases = [l.strip() for l in open("wordlists/implicative_verbs.txt")]
split_implicative_phrases = [p.split() for p in implicative_phrases]
implicative_phrase_dict = {p.split()[0]: p.split() for p in implicative_phrases} # a dictionary mapping each implicative verb to the implicative phrase
implicative_verbs = [p[0] for p in split_implicative_phrases]# the list of implicative verbs

file = open("../COCA_sample_10MB.txt")
output = open("outputs/implicative_verbs.txt", "w")

nlp = spacy.load("en_core_web_sm")
context_buffer = ["", ""]

for line in file:
    doc = nlp(line)
    for sentence in doc.sents:
        impl_verbs = [t for t in sentence if t.text in implicative_verbs]
        if len(impl_verbs) > 0:
            for impl_verb in impl_verbs:
                impl_children = [c for c in impl_verb.children if c.dep_ == "xcomp" and c.pos_ == "VERB"]
                if len(impl_children) > 0:
                    example = {
                        "sentence": sentence.text.strip(),
                        "context1": context_buffer[0].strip(),
                        "context2": context_buffer[1].strip(),
                        "implicative": impl_verb.text
                    }
                    output.write(str(example) + "\n")
                    print(sentence.text.strip())
                    output.flush()
                    break
        context_buffer.pop(0)
        context_buffer.append(sentence.text)

#TODO: Limit sentence length
#TODO: add more predicates
#TODO: get rid of embedded questions