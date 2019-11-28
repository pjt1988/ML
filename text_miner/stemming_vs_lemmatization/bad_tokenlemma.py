import nltk
import nltk.corpus
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer() 
from nltk.stem import PorterStemmer
pst = PorterStemmer()
#tokenize text, analyse frequency of words. need to find root for words, ie driving -> drive. 

text = "Friends, romans, countrymen. Lend me your ears. I have come to bury caesar, not to praise him. The noble brutus hath told you caesar was ambitious. If it were so it was a grievous fault. And grievously something something something. tenth grade english was a while back."

token = word_tokenize(text)
print(token)
tags = nltk.pos_tag(token)
print(tags)

lemma = lemmatizer.lemmatize(text)
print(lemma)

test = lemmatizer.lemmatize("testing")
print(test)
print("rocks :", lemmatizer.lemmatize("rocks"))

print("corpus : ", lemmatizer.lemmatize("corpus"))

