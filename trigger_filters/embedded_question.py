import spacy
import numpy as np

wh_predicates = [l.strip() for l in open("wh_predicates.txt")]
print(wh_predicates)

file = open("/Users/alexwarstadt/Workspace/data/bnc/bnc.txt")
output = open("outputs/embedded_question.txt", "w")

presuppositional_wh_words = ["what", "who", "which", "when", "where", "why", "how"]


context_buffer = [next(file), next(file)]
for line in file:
    words = line.lower().split()
    wh_verbs = np.intersect1d(words, wh_predicates)
    if len(wh_verbs) > 0:
        for wh_verb in wh_verbs:
            if len(words) > words.index(wh_verb) + 1 and words[words.index(wh_verb) + 1] in presuppositional_wh_words:
                if len(words) > words.index(wh_verb) + 2 and words[words.index(wh_verb) + 2] != "to":
                    for s in context_buffer:
                        output.write(s)
                    print(line)
                    output.write(line + "\n")
                    output.flush()
                    break
    context_buffer.pop(0)
    context_buffer.append(line)

# TODO: Limit to realis uses
# TODO: Limit by length of sentence
# TODO: Add more predicates