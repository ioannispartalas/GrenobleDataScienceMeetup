#!/bin/bash

DATA="./data"
MODEL_PATH="./"

train_data=$1
test_data=$2
prediction="preds_vw.txt"

EVAL="perl connlleval.pl"

#echo "Vectorizing"
python NerVectorizer.py $train_data ./tmp_train.txt 
python NerVectorizer.py $test_data ./tmp_test.txt 

#echo "Training"
options="-b 29 --quiet --search 3 --affix -3w,3w --search_task sequence --search_neighbor_features -1:w,1:w,-1:pos,-1:N,1:N,-2:w,2:w --search_history_length 2 --passes 10 --learning_rate 0.07492 -c -k --holdout_off"
model_name="vw_model.model"

train_command="vw ${options}  tmp_train.txt -f ${MODEL_PATH}${model_name}"
#echo $train_command
test_command="vw --quiet -t -i ${MODEL_PATH}${model_name} tmp_test.txt -p ${prediction}"

eval "${train_command}"
#echo "Saving in ${MODEL_PATH}"
eval "${test_command}"
#echo "Evaluating"
eval "cat ${prediction}| sed -e 's/ /\n/g' | python inverse_labels.py | paste data/example_data.txt - | tr '\t' ' ' | ${EVAL}"
#echo "Cleaning"
eval "rm tmp_train.txt* tmp_test* $prediction ${MODEL_PATH}${model_name}"
