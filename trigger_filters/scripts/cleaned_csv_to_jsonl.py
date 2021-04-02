import sys
import csv
import json



with open(sys.argv[1], "r") as csv_f, open(sys.argv[2], "w") as out_f:
  reader = csv.DictReader(csv_f)
  for line in reader:
    if "presupposition_corrected" in line:
      if len(line["presupposition_corrected"].strip()) > 0:
        line["presupposition"] = line["presupposition_corrected"]
    
      del line["presupposition_corrected"]
    
    
    if "sentence with restriction" in line:
      line["sentence"] = line["sentence with restriction"]
      line["negated_sentence"] = line["negated sentence with restriction"]
      line["presupposition"] = line["presupposition with restriction"]
      del line["sentence with restriction"]
      del line["negated sentence with restriction"]
      del line["presupposition with restriction"]
    
    print(json.dumps(line), file=out_f)
