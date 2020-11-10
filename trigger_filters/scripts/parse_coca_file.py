#!/usr/bin/env python

import sys, argparse, os
import spacy
from spacy_conll import ConllFormatter
from lib.coca_document_parser import COCADoc


def main():
    parser = argparse.ArgumentParser(description='Dependency parse individual COCA file with spacy.')
    parser.add_argument('--input', help='Path to COCA corpus file')
    parser.add_argument("--output-dir", default="./parsed/", help="Output path for parsed files")
    args = parser.parse_args()

    nlp = spacy.load("en_core_web_sm")
    conllformatter = ConllFormatter(nlp)
    nlp.add_pipe(conllformatter, last=True)

    if not os.path.isdir(args.output_dir):
        os.mkdir(args.output_dir)

    base_name = os.path.basename(args.input).replace(".txt", "")
    with open(args.input, 'r') as corpus_f:
        for line in corpus_f:
            coca_doc = COCADoc(line)
            doc_id = coca_doc.doc_id.replace("@@", "")
            for segment_no, segment in enumerate(coca_doc.segments):

                out_file_name = f"{base_name}-{doc_id}-{segment_no+1}.conll"
                out_file_path = os.path.join(args.output_dir, out_file_name)

                # write each segment to it's own output file
                # (should make trigger extraction easier)
                with open(out_file_path, "w") as out_f:
                    for speaker, turn_content in segment.turns:
                        turn_content = turn_content.strip()
                        if len(turn_content) < 1:
                            continue

                        # parse sentence
                        spacy_doc = nlp(turn_content)
                        for sentence in spacy_doc.sents:
                            # write metadata to CoNLL file
                            print(f"# text = {sentence}", file=out_f)
                            print(f"# doc_id = {coca_doc.doc_id}", file=out_f)
                            print(f"# segment_id = {coca_doc.doc_id}-{segment_no+1}", file=out_f)
                            print(f"# speaker = {speaker}", file=out_f)

                            # write parse to CoNLL file
                            print(sentence._.conll_str, file=out_f)


if __name__ == '__main__':
    main()
