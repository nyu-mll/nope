# Copyright (c) 2017-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
#

preprocess_exec="sed -f tokenizer.sed"

SNLI='https://nlp.stanford.edu/projects/snli/snli_1.0.zip'
MultiNLI='https://cims.nyu.edu/~sbowman/multinli/multinli_1.0.zip'
ANLI='https://dl.fbaipublicfiles.com/anli/anli_v1.0.zip'


ZIPTOOL="unzip"


### download SNLI
mkdir SNLI
curl -Lo SNLI/snli_1.0.zip $SNLI
$ZIPTOOL SNLI/snli_1.0.zip -d SNLI
rm SNLI/snli_1.0.zip
rm -r SNLI/__MACOSX

# download MultiNLI
# Test set not available yet : we define dev set as the "matched" set and the test set as the "mismatched"
mkdir MultiNLI
curl -Lo MultiNLI/multinli_1.0.zip $MultiNLI
$ZIPTOOL MultiNLI/multinli_1.0.zip -d MultiNLI
rm MultiNLI/multinli_1.0.zip
rm -r MultiNLI/__MACOSX

# download ANLI
mkdir ANLI
curl -Lo ANLI/anli_1.0.zip $ANLI
$ZIPTOOL ANLI/anli_1.0.zip -d ANLI
rm ANLI/anli_1.0.zip

# call python script to combine all train/test/dev sets from 3 SNLI/MNLI/ANLI
python combine_datasets.py

# tokenize combined dataset
for x in combined/*
do
    $preprocess_exec $x > $x.temp
    mv $x.temp $x
done
