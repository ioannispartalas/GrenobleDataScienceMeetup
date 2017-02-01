# GrenobleDataScienceMeetup

A hands-one session for the Grenoble Data Science Meetup presented with Georgios Balikas.

The session concerns the development of models for the task of Named Entity Recognition (NER) in tweets.

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

In NER the goal is to identify the named entities that appear in textual segment and 
classify in a predefined set of categories. Foe example, such an entity could be
a person, an organization, a music-artist or an event. The following figure presents
an example of a tweet which contains two named entities.

![Ner task](images/ner_fig.png?raw=true "A tweet with named entities")

## Data

Our data consists of tweets which are structured according to CoNLL format where each line
contains a line with the token and its label separated by white space. For the encoding
of the labels we will follow the BIO encoding where for the first token of an entity *X*
the label *B-X* is attributed while for the tokens inside the entity the label *I-X*.
For all other tokens we use the label *O* (out).

Here is an example using the above format:

| Token | Label |
|---|---:|
| Paris | B-sportsteam |
| Saint | I-sportsteam |
| \- | I-sportsteam |
| Germain | I-sportsteam |
| will | O |
| play | O |
| against | O |
| Nice | B-sportsteam |
| in | O |
| PdP | B-facility |


## Requirements
* Basic python installation 
* You should have Vowpall Wabbit installed in the path as vw. Please check installation instructions in the [VW tutorial page](https://github.com/JohnLangford/vowpal_wabbit/wiki/Tutorial).

## Docker

A docker file is also provided for building a functional environment.

You should have Docker installed in your system. For building the image give the following command inside the folder of the project.

```
sudo docker build -f DockerFile -t meetup .
```

This step may take some time, so keep cool. 

After the image is built you can start an interactive shell with the following command:

```
sudo docker run  --name meetup_container -t -i  meetup
```

## References
[1] Partalas, Ioannis, Lopez, Cédric, Derbas, Nadia  and  Kalitvianski, Ruslan, Learning to Search for Recognizing Named Entities in Twitter, Proceedings of the 2nd Workshop on Noisy User-generated Text (WNUT), COLING 2016
