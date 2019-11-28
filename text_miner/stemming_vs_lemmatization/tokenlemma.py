#taken from
#https://www.analyticsvidhya.com/blog/2018/02/the-different-methods-deal-text-data-predictive-python/

import pandas as pd
from nltk.corpus import stopwords
stop = stopwords.words('english')
from textblob import Word


from textblob import TextBlob
wrong = "ths is wrng. too mny spalling misteaks"
print(wrong)
print(str(TextBlob(wrong).correct()))
#correct does not work inplace...
lem = "the quick brown fox jumped over the dawg. well better good goodly bad badly jump jumps jumping jumped person people train trains"
print(lem)
lem = TextBlob(lem)
print(lem.tags)
lemmat = []
for x in lem.split():
    lemmat.append(Word(x).lemmatize())
print(lemmat)
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
