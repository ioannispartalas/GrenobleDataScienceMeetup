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

## Requierements

You should have Vowpall Wabbit installed in the path as vw.
