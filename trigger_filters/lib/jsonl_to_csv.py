import sys
from random import shuffle
import csv

input_f = open(sys.argv[1], mode='r')
num_examples = int(sys.argv[2])

examples = [eval(line) for line in input_f]
shuffle(examples)
with open(".".join(sys.argv[1].split(".")[:-1] + ["tsv"]), "w") as output_f:
    header = examples[0].keys()
    cw = csv.DictWriter(output_f, header, delimiter='\t')
    cw.writeheader()
    cw.writerows(examples[:num_examples])
    # output_f.write("\t".join(examples[0].keys()) + "\r\n")
    # for e in examples[:num_examples]:
    #     print(len(e.values()))
    #     output_f.write("\t".join(e.values()) + "\r\n")
