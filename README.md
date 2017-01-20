# GrenobleDataScienceMeetup

A hands-one session for the Grenoble Data Science Meetup presented with Georgios Balikas.

The session concerns the developement of models for the task of Named Entity Recognition in tweets.

To train and evaluate the model just give the following command:

`
./train_and_test_vw.sh path_to_train_data path_to_test_data
`

For a sanity check give the following:

`
./train_and_test_vw.sh data/example_data.txt data/test_data.txt
`

If everything goes well and our model fits nicely the data you should get an F-score of 100%.

## The task

## Data

Our data will consist of tweets which will be formatted according to CoNLL format where each line
contains a line with the token and its label separated by white space. For the encoding
of the labels we will follow the BIO encoding where for the first token of an entity *X*
the label *B-X* is attributed while for the tokens inside the entity the label *I-X*.
For all other tokens we use the label *O* (out).

Here is an example using the above format:

Paris	B-sportsteam
Saint	I-sportsteam
-	I-sportsteam
Germain	I-sportsteam
will	O
play 	O
against	O
Nice	B-sportsteam
in	O
PdP	B-facility


## Requierements

You should have Vowpall Wabbit installed in the path as vw.
