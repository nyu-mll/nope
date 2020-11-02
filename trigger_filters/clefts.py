import spacy
import numpy as np

#coca = tarfile.open("C:/Users/NYUCM Loaner Access/Documents/GitHub/SECRET/COCA.tar")
#coca.extractall()
coca1 = open("COCA/COCA Text/text_fiction_awq/2012_fic.txt")
cleft_file = open("C:/Users/NYUCM Loaner Access/Documents/GitHub/presupposition_dataset/trigger_filters/outputs/clefts.txt", "w")

cleft_prefixes = ["it"]
be_verb = ["'s", "is", "was"]
determiners = ["the", "my"]
comp = ["who", "that"]

context_buffer = [next(coca1), next(coca1)]
for line in coca1:
    words = line.lower().split()
    cleft_word = np.intersect1d(words, cleft_prefixes)
    if len(cleft_word) > 0:
        if words[words.index(cleft_word) + 1] in be_verb:
            if words[words.index(cleft_word) + 2] in determiners:
                if len(words) > words.index(cleft_word) + 3 and len(np.intersect1d(words[words.index(cleft_word) + 3:], comp)) > 0:
                    for s in context_buffer:
                        cleft_file.write(s)
                    print(line)
                    cleft_file.write(line + "\n")
                    cleft_file.flush()
    context_buffer.pop(0)
    context_buffer.append(line)
cleft_file.close()
