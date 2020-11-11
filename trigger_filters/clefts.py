import spacy
import numpy as np

coca1 = open("C:/Users/NYUCM Loaner Access/Documents/GitHub/presupposition_dataset/COCA_sample_10MB.txt")
cleft_file = open("C:/Users/NYUCM Loaner Access/Documents/GitHub/presupposition_dataset/trigger_filters/outputs/clefts.txt", "w")

cleft_prefixes = ["it"]
be_verb = ["'s", "is", "was"]
determiners = ["the", "my"]
comp = ["who", "that"]

#initialize spacy processor
nlp = spacy.load("en_core_web_sm")

def check_cleft(sentence):
    tokens = list(sentence)
    tokens_str = [str(token) for token in tokens]
    cleft_word = np.intersect1d(tokens_str, cleft_prefixes)  # get any cleft prefixes in appear in the sentence
    if len(cleft_word) > 0 and tokens_str.index(cleft_word) + 3 <= len(
            tokens_str):  # if the list of cleft prefixes is non-empty and there's sufficient words following it:
        if tokens_str[tokens_str.index(cleft_word) + 1] in be_verb:  # if the word after the cleft prefix is a form of 'to be':
            cop = tokens[tokens_str.index(cleft_word) + 1]
            obj = None
            for child in cop.children:
                #print(child.dep_,child.text)
                if child.dep_ in ['attr','dobj']:
                    obj = child
                    break
            if obj is not None:
                for child in obj.children:
                    if child.dep_ in ['ccomp', 'relcl']:
                        for child2 in child.children:
                            if child2.text in comp:
                                return True
    return False

counter=0
for line in coca1:
    doc = nlp(line)
    context_buffer = ["", ""]
    for sentence in doc.sents:
        if check_cleft(sentence):
            counter += 1
            print(counter)
            cleft_dict = {"context1": context_buffer[0], "context2":context_buffer[1],"sentence": sentence.text.strip()}
            cleft_file.write(str(cleft_dict) + "\n")
            cleft_file.flush()
        context_buffer.pop(0)
        context_buffer.append(sentence.text.strip())
    # counter+=1
    # if counter > 1000:
    #     break

cleft_file.close()
