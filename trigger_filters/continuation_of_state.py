import spacy
import argparse
import json

from lib.coca_document_parser import COCADoc

nlp = spacy.load("en_core_web_sm")

def extract_examples_from_segment(segment, cos_predicates):
    context_buffer = [(None, ""), (None, "")]
    for speaker, turn_content in segment.turns:
        spacy_doc = nlp(turn_content)
        for sentence in spacy_doc.sents:
            for token in sentence:
                if str(token) in cos_predicates and token.tag_[0] == "V" and token.dep_ == "ROOT":
                    include = False
                    for child in token.children:
                        if child.dep_ in ["xcomp", "ccomp"]:
                            include = True
                            break
                    if include:
                        yield (context_buffer, speaker, sentence, str(token))
                    break
            context_buffer.pop(0)
            context_buffer.append((speaker, sentence))


def example_to_jsonl(ex):
    context_buffer, target_speaker, target_sentence, target_token  = ex
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

    with  open(corpus_path, 'r') as corpus, open(output_path, 'w') as out_f:
        cnt = 0
        for line in corpus:
            coca_doc = COCADoc(line)
            for segment in coca_doc.segments:
                words = segment.raw_segment.lower().split()
                if set(words) & change_of_state_predicates:
                    for ex in extract_examples_from_segment(segment, change_of_state_predicates):
                        print(example_to_jsonl(ex), file=out_f)
            cnt +=1
            if cnt % 100 == 0:
                print(f"Processed {cnt} documents...")





        #    for s in context_buffer:
        #        output.write(s)
    #        output.write(line + "\n")
#            output.flush()
#        context_buffer.pop(0)
    #    context_buffer.append(line)




# TODO: I could limit to the matrix verb
# TODO: I could limit length of sentence
# TODO: I could limit to realis uses
# TODO: Add more predicates


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Extract continuation of state peredicates.')
    parser.add_argument('--corpus', default="../../corpora/COCA_Sample_13.4MB.txt",
                    help='Path to COCA corpus')
    parser.add_argument('--cos-predicates', default="./wordlists/continuation_of_state_predicates.txt",
                        help='Path to list with continuation of state predicates (one predicate per line)')
    parser.add_argument("--output", default="./outputs/continuation_of_state.jsonl")
    args = parser.parse_args()

    main(args.corpus, args.cos_predicates, args.output)
