import sys
from random import shuffle
import csv


triggers = [
            "clefts",
            "comparatives",
            "continuation_of_state",
            "embedded_question",
            "factives",
            "implicative_predicates",
            "re_verbs",
            # "temporal_adverbs"
            ]
header = ["trigger", "context1_speaker", "context1", "context2_speaker", "context2", "sentence", "trigger_data", "speaker",
          "appropriate?", "negatable?", "negated_sentence", "presupposition",
          "Pr(H|C)", "Pr(H|C+P)", "Pr(H|C+~P)", "notes"]
num_examples = 120
people = ["alex", "alicia", "omar", "sebastian", "soo-hwan", "zhuoye"]
outputs = {}
for p in people:
    f = open(f"../annotation/{p}.tsv", "w")
    outputs[p] = csv.DictWriter(f, header, delimiter='\t')
    outputs[p].writeheader()

def standardize_dict(example, header, trigger):
    # examples = [eval(line) for line in open(input_f)]
    new_example = {}
    for h in header:
        if h in example:
            new_example[h] = example[h]
        else:
            new_example[h] = ""
    new_example["trigger_data"] = {}
    for k in example.keys():
        if k not in header:
            new_example["trigger_data"][k] = example[k]
    new_example["trigger_data"] = str(new_example["trigger_data"])
    new_example["trigger"] = trigger
    return new_example


for trigger in triggers:
    input_f = f"../outputs/{trigger}.jsonl"
    examples = [eval(line) for line in open(input_f)]
    shuffle(examples)
    n = min(num_examples, len(examples))
    examples = [standardize_dict(e, header, trigger) for e in examples[:n]]
    indices = [int(i * n/6) for i in range(7)]
    for i, p in enumerate(people):
        outputs[p].writerows(examples[indices[i]:indices[i+1]])



# with open(".".join(input_f.split(".")[:-1] + ["tsv"]), "w") as output_f:
#     cw = csv.DictWriter(output_f, header, delimiter='\t')
#     cw.writeheader()
#     cw.writerows(examples[:num_examples])
