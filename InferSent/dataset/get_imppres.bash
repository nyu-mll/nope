rm -rf imppres
mkdir imppres

wget https://github.com/facebookresearch/Imppres/archive/refs/heads/master.zip
unzip master.zip
mv Imppres-master/dataset/presupposition/* imppres
rm master.zip
rm -rf Imppres-master
cat imppres/* > imppres/imppres_all.jsonl
sed -i '.bak' -e 's/sentence1/premise/' imppres/imppres_all.jsonl
sed -i '.bak' -e 's/sentence2/hypothesis/' imppres/imppres_all.jsonl
#
#for x in all_n_presupposition both_presupposition change_of_state cleft_existence cleft_uniqueness question_presupposition
#do
#  wget https://raw.githubusercontent.com/facebookresearch/Imppres/master/dataset/presupposition/$x.jsonl
#  mv $x.jsonl imppres
##  sed -i '.bak' -e 's/sentence1/premise/' imppres/$x
##  sed -i '.bak' -e 's/sentence2/hypothesis/' imppres/$x
#  cat imppres/$x > imppres_all.jsonl
#done