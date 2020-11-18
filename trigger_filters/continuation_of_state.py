import argparse
import json
import spacy

# import CoNLLReader class
from lib.conll_reader import CoNLLReader

def example_to_jsonl(context_buffer, target_speaker, target_sentence, target_token):
    obj = {
            "context1_speaker": context_buffer[0][0],
            "context1": str(context_buffer[0][1]),
            "context2_speaker": context_buffer[1][0],
            "context2": str(context_buffer[1][1]),
            "sentence": str(target_sentence),
            "speaker": target_speaker,
            "predicate": target_token
    }
    return json.dumps(obj)



def main(corpus_path, cos_predicate_path, output_path):

    with open(cos_predicate_path, 'r') as f:
        change_of_state_predicates = set([l.strip() for l in f])

    with open(output_path, 'w') as out_f:

        # initialize the context buffer
        context_buffer = [(None, ""), (None, "")]

        # keep track of current segment name
        prev_segment_name = ""
        cnt = 0

        # loop through parsed sentences
        # sentence is a scipy "Doc" object
        for sentence, metadata in CoNLLReader(corpus_path):

            # check if the segment changed and reset context buffer
            if prev_segment_name != metadata["segment_id"]:
                context_buffer = [(None, ""), (None, "")]
                prev_segment_name = metadata["segment_id"]

            # extract words as list of strings
            words = [t.text for t in sentence]

            # extract speaker
            speaker = metadata["speaker"]

            if set(words) & change_of_state_predicates:
                for token in sentence:
                    if (str(token) in change_of_state_predicates
                      and token.tag_[0] == "V"
                      and token.dep_ == "ROOT"):
                        include = False
                        for child in token.children:
                            if child.dep_ in ["xcomp", "ccomp"]:
                                include = True
                                break

                        if include:
                            # write example to jsonl file
                            out_f.write(example_to_jsonl(context_buffer, speaker, sentence, str(token)))
                            out_f.write("\n")
                            break

            # update context buffer
            context_buffer.pop(0)
            context_buffer.append((speaker, sentence))

            # print status updates
            cnt +=1
            if cnt % 100 == 0:
                print(f"Processed {cnt} sentences...")



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Extract continuation of state peredicates.')
    parser.add_argument('--corpus', default="../../corpora/COCA_Sample_13.4MB.txt",
                    help='Path to COCA corpus')
    parser.add_argument('--cos-predicates', default="./wordlists/continuation_of_state_predicates.txt",
                        help='Path to list with continuation of state predicates (one predicate per line)')
    parser.add_argument("--output", default="./outputs/continuation_of_state.jsonl")
    args = parser.parse_args()

    main(args.corpus, args.cos_predicates, args.output)
