import sys

label_mapping = {'O':1,'B-person':2,'I-person':3,'B-company':4,'I-company':5,'B-facility':6,'I-facility':7,'B-geo-loc':8,'I-geo-loc':9,
        'B-movie':10,'I-movie':11,'B-musicartist':12,'I-musicartist':13,'B-other':14,'I-other':15,'B-product':16,'I-product':17,'B-sportsteam':18,
        'I-sportsteam':19,'B-tvshow':20,'I-tvshow':21}

inv_mapping = dict((v,k) for k,v in label_mapping.iteritems())

for line in sys.stdin:
    line = line.strip('\n').strip('\r')
    if not line:
        sys.stdout.write("\n")
    else:
        sys.stdout.write(inv_mapping[int(line)]+"\n")
