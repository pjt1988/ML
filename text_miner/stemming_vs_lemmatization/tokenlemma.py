#taken from
#https://www.analyticsvidhya.com/blog/2018/02/the-different-methods-deal-text-data-predictive-python/
#https://www.machinelearningplus.com/nlp/lemmatization-examples-python/

import pandas as pd
from nltk.corpus import stopwords
stop = stopwords.words('english')
from textblob import Word
import nltk
from nltk.stem import WordNetLemmatizer 

nl_lem = WordNetLemmatizer()

from nltk.corpus import wordnet

#pip install is broken. first, pip install pdfminer==20140328. then install pattern. yes, this version. 

import pattern
from pattern.en import lemma, lexeme


#for textblob
tag_dict = {"J": 'a',
                "N": 'n',
                "V": 'v',
                "R": 'r'}

def get_wordnet_pos(word):
    """Map POS tag to first character lemmatize() accepts"""
    tag = nltk.pos_tag([word])[0][1][0].upper()
    tag_dict = {"J": wordnet.ADJ,
                "N": wordnet.NOUN,
                "V": wordnet.VERB,
                "R": wordnet.ADV}

    return tag_dict.get(tag, wordnet.NOUN)


from textblob import TextBlob
wrong = "ths is wrng. too mny spalling misteaks"
print(wrong)
print(str(TextBlob(wrong).correct()))
#correct does not work inplace...
lem = "the quick brown fox jumped over the dawg. well better good goodly bad badly jump jumps jumping jumped person people train trains"
#lem = "The striped bats are hanging on their feet for best"
print(lem)
lem2 = TextBlob(lem)
print(lem2.tags)
words_and_tags = [(x, tag_dict.get(pos[0], 'n')) for x, pos in lem2.tags]    
lemmatized_list = [wd.lemmatize(tag) for wd, tag in words_and_tags]
lemmat = []
for x in lem.split():
    lemmat.append(Word(x).lemmatize())
print("wordblob lemmatize:")
print(lemmat)
print("nltk lemmatize via tags")
nltk_lem_tags = [nl_lem.lemmatize(x, get_wordnet_pos(x)) for x in nltk.word_tokenize(lem)]
print(nltk_lem_tags)
print(" ".join(nltk_lem_tags))
print("wordblob lemmatize + tags")
print(lemmatized_list)
print(" ".join(lemmatized_list))
print("pattern lemmatize + tags")
print([lemma(x) for x in lem.split()])
print(" ".join([lemma(x) for x in lem.split()]))
exit(1)



train = pd.read_csv('train_E6oV3lV.csv')
train['hashtags'] = train['tweet'].apply(lambda x: [x.lower() for x in x.split() if x.startswith('#')])
train['tweet'] = train['tweet'].str.replace('[^\w\s]','')
train['tweet'][:5] = train['tweet'][:5].apply(lambda x: [str(TextBlob(x).correct())])
train['tweet'] = train['tweet'].apply(lambda x: " ".join([Word(y).lemmatize() for y in str(x).split()]))
train['word_count'] = train['tweet'].apply(lambda x: len(str(x).split(" ")))
train['char_count'] = train['tweet'].apply(lambda x: sum(len(word) for word in str(x).split()))
train['stop_count'] = train['tweet'].apply(lambda x: len([x.lower() for x in x.split() if x in stop]))
train['nonstop'] = train['tweet'].apply(lambda x: [x.lower() for x in x.split() if x not in stop])
train['tweet_adj'] = train['tweet'].apply(lambda x: [x.lower() for x in x.split() if x not in stop])



#find rarerest and most common words, and removes them from the text dump
bfreq = pd.Series(' '.join(train['tweet']).split()).value_counts()[-10:]
tfreq = pd.Series(' '.join(train['tweet']).split()).value_counts()[10:]
print(bfreq)
print(tfreq)
train['tweet_adj'].apply(lambda x: " ".join(x for x in x if x not in bfreq))
train['tweet_adj'].apply(lambda x: " ".join(x for x in x if x not in tfreq))

print(train[['tweet','word_count','stop_count','tweet_adj']][0:5])
