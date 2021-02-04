import sys
import csv
import json



with open(sys.argv[1], "r") as csv_f, open(sys.argv[2], "w") as out_f:
  reader = csv.DictReader(csv_f)
  for line in reader:
    if len(line["presupposition_corrected"].strip()) > 0:
      line["presupposition"] = line["presupposition_corrected"]
    
    del line["presupposition_corrected"]
    print(json.dumps(line), file=out_f)
