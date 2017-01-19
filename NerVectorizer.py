import nltk
import codecs
import sys,os
import re,time
import numpy as np
import itertools

# Class for vectorizing textual data in ConLL format


class NerVectorizer:
    
    emoticons = {":)":"happy",";)":"happy",":D":"happy",":>":"happy",":o":"surprise",":P":"tongues",":-p":"tongues",":-)":"happy",":-D":"happy",
        ":(":"sad",":-(":"sad",":-|":"sad",";-(":"sad","=\\":"unhappy",":\\":"unhappy",":/":"unhappy",":-/":"unhappy",":O":"surprised",":]":"happy",":?":"thinking",":p":"tongues"}
   
    
    
    def __init__(self,is_test,sep='\t'):
        self.is_test = is_test
        self.sep = sep
        self.X_sentences=[] # here we will keep the examples

        # We use the following mapping for the entity tags to be used in the ML algorithm
        self.label_mapping = {'O':1,'B-person':2,'I-person':3,'B-company':4,'I-company':5,'B-facility':6,'I-facility':7,'B-geo-loc':8,'I-geo-loc':9,
        'B-movie':10,'I-movie':11,'B-musicartist':12,'I-musicartist':13,'B-other':14,'I-other':15,'B-product':16,'I-product':17,'B-sportsteam':18,
        'I-sportsteam':19,'B-tvshow':20,'I-tvshow':21}
        
    # yield a dictionary for each sentence in the file
    # We initialize with the token (w) and the label (y)
    def data_iter(self,infile):
        sep = self.sep
        X = []
        for line in infile:
            line = line.strip('\n').strip('\r').strip()
            if not line:
                yield X
                X = []
            else:
                fields = line.split(sep)
                item = {}
                item['w'] = fields[0]
                if len(fields)>1:
                    item['y'] = fields[1] # label of the word
                else: # for the test set
                    item['y'] = "O"
                X.append(item)
    

    def read_data(self,infile):
        sentences = []
        for sentence in self.data_iter(infile):
            sentences.append(sentence)
        print("Found "+str(len(sentences))+" tweets")
        self.X_sentences = sentences


    def OrthographicFeats(self,w):
        features = {'init_cap':0,'all_cap':0,'contains_cap_letter':0,'is_digit':0,'has_digit':0,'has_dash':0,'punct':0,'istime':0,'IS_hashtag':0,
                'starts_with_@':0,'istime':0,'starts_with_http':0}

       
        if re.search(r'^[A-Z]',w):
            features['init_cap'] = 1
        if w.isupper():
            features['all_cap'] = 1
        if re.match(r'.*[A-Z].*',w):
            features['contains_cap_letter'] = 1
        if w.isdigit():
            features['is_digit'] = 1
        if re.match(r'.*[0-9].*',w):
            features['has_digit'] = 1
        if re.match(r'.*-.*', w):
            features['has_dash']=1
        if re.match(r'[.,;:?!-+\'"]', w):
            features['punct'] = 1
        if re.match(r'[0-9]+:[0-9]+',w):
            features['istime']=1
        if w.startswith("#"):
            features['IS_hashtag']=1
        if w.startswith("@"):
            features['starts_with_@']=1

        if w == "USER_PLACEHOLDER":
            features['starts_with_@']=1
            
        if w == "URL":
            features['starts_with_http']=1
        if w == "time_placeholder":
            features['istime'] = 1
        
        return features


    def preprocess(self,w):
        w_re = w
        if re.match(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',w):
            w_re = "URL"
        em =  NerVectorizer.emoticons.get(w)
        if em != None:
            w_re = em
        if re.match(r'^@\w',w):
            return "USER_PLACEHOLDER"
        if w == ":":
            return "COLON"
        if w == "|":
            return "VERT_LINE"
        if re.match(r'&amp;',w):
            return "&"
        if re.match(r'&gt;',w):
            return ">"
        if re.match(r'&lt;',w):
            return "<"
        if re.match(r'[0-9]+:[0-9]+',w):
            return "time_placeholder"
        if re.match(r'.*:.*',w):
            return 'colon_placeholder'
        w_re = re.sub(r"\|","_",w_re)
        return w_re


    # takes a dictionary with word and label and outputs features
    def featurize(self,X):
        if X:
            for t in range(len(X)):
                X[t]['w'] = self.preprocess(X[t]['w'])
                w = X[t]['w']
                w_lower = w.lower()
                feats = self.OrthographicFeats(w)
                X[t]['F'] = feats
                
         
    def to_vw(self,X):
        s=""
        for t in range(len(X)):
            s+=str(self.label_mapping[X[t]['y']])+" |"
            s+="w "+X[t]['w']
            for namespace in ['F']:
                s+=" |"+namespace
                if type(X[t][namespace]) is dict:
                    for feat in X[t][namespace]:
                        if type(X[t][namespace][feat]) is int:
                            if X[t][namespace][feat]!=0:
                                s+=" "+feat
                        else:
                            s+=" "+str(X[t][namespace][feat])
                    s+="\n"
        return s

    def to_str(self):
        for x in self.X_sentences:
            print x

    def sentence_to_string(sentence):
        s=""
        for t in range(len(sentence)):
            s+=sentence[t]['w']+" "
        return s


    def vectorize_with_types(self,out_filename):
        X_sentences = self.X_sentences
        out = codecs.open(out_filename,'w',encoding='utf-8')

        print("Writing to "+out_filename)
        for sent in X_sentences:
            self.featurize(sent)
            s = self.to_vw(sent)
            out.write(s)
            out.write("\n")
        out.close()

    # Featurize the dataset and write to file
    def transform(self,outfile):
        self.vectorize_with_types(outfile)

if __name__=='__main__':
    ner_vect = NerVectorizer(False)
    infile = codecs.open(sys.argv[1],encoding='utf-8')
    ner_vect.read_data(infile)
    ner_vect.transform(sys.argv[2])
