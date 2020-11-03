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

for line in coca1:
    lines = line.split("#")
    for i in range(1, len(lines)):
        this_line = ''.join(map(str, lines[i]))
        words = this_line.lower().split()
        cleft_word = np.intersect1d(words, cleft_prefixes)
        if len(cleft_word) > 0 and words.index(cleft_word)+3 <= len(words):
            if words[words.index(cleft_word) + 1] in be_verb:
                if words[words.index(cleft_word) + 2] in determiners:
                    if len(np.intersect1d(words[words.index(cleft_word) + 3:], comp)) > 0:
                        if len(words) < words.index(cleft_word) + 8:
                            print(this_line)
                            prev_line = ''.join(map(str, lines[i-1]))
                            cleft_file.write(prev_line)
                            cleft_file.write(this_line + "\n" + "\n")
                            cleft_file.flush()
                        elif len(np.intersect1d(words[words.index(cleft_word) + 3:words.index(cleft_word) + 8], comp)) > 0:
                            print(this_line)
                            prev_line = ''.join(map(str, lines[i - 1]))
                            cleft_file.write(prev_line)
                            cleft_file.write(this_line + "\n" + "\n")
                            cleft_file.flush()

cleft_file.close()
