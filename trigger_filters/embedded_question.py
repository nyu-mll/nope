import spacy
import numpy as np
from pragmatics_dataset.trigger_filters.spacy_utils import get_dependents_string


nlp = spacy.load("en_core_web_sm")
wh_predicates_1_word = [l.strip().split()[0] for l in open("wordlists/wh_predicates.txt")]
wh_predicates_n_words = [l.strip() for l in open("wordlists/wh_predicates.txt")]
# print(wh_predicates)

file = open("/Users/alexwarstadt/Workspace/data/bnc/bnc.txt")
output = open("outputs/embedded_question.jsonl", "w")

presuppositional_wh_words = ["what", "who", "which", "when", "where", "why", "how"]


def sentence_contains_embedded_question(sentence):
    if len([wh for wh in wh_predicates_n_words if wh in sentence.text]) > 0:    # are there wh predicates in the sentence?
        wh_predicates_in_sentence = [t for t in sentence if t.lemma_ in wh_predicates_1_word]
        for wh_predicate in wh_predicates_in_sentence:     # do any of the wh predicates actually have a wh-clause
            ccomp_children = [c for c in wh_predicate.children if c.dep_ == "ccomp"]
            if len(ccomp_children) > 0:  # NOTE: You could exclude sentences with embedded clauses inside the complement clause, to make judgments simpler
                for c in ccomp_children:    # is the embedded clause interrogative?
                    try:
                        if next(c.children).text in presuppositional_wh_words:
                            embedded_q = get_dependents_string(c)
                            return True, embedded_q, wh_predicate
                    except Exception:
                        continue
    return False, None, None


def get_embedded_question_sentences():
    context_buffer = ["", ""]
    for line in file:
        doc = nlp(line)
        for sentence in doc.sents:
            passes, embedded_q, wh_predicate = sentence_contains_embedded_question(sentence)
            if passes:
                example = {
                    "sentence": sentence.text.strip(),
                    "context1": context_buffer[0].strip(),
                    "context2": context_buffer[1].strip(),
                    "wh_predicate": wh_predicate.text,
                    "embedded_question": embedded_q
                }
                output.write(str(example) + "\n")
                output.flush()
            context_buffer.pop(0)
            context_buffer.append(sentence.text)


# ======== MAIN =========
get_embedded_question_sentences()


# TODO: Limit to realis uses ?
# TODO: Limit by length of sentence ?