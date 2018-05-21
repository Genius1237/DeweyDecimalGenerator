from nltk.classify import NaiveBayesClassifier
from nltk.corpus import stopwords,wordnet
from nltk.tokenize import sent_tokenize, word_tokenize, TreebankWordTokenizer, WordPunctTokenizer
import random

def get_antonym(word):
    antonyms=set()
    for syn in wordnet.synsets(word):
        for lemma in syn.lemmas():
            for antonym in lemma.antonyms():
                antonyms.add(antonym.name())
    if len(antonyms) != 0:
        return random.sample(antonyms,1)[0]
    else:
        return ""

def replace_antonyms(words):
    i=0
    l=len(words)
    for i in range(l):
        if words[i]=='not' and i+1<l:
            ant=get_antonym(words[i+1])
            if ant !="":
                words[i]=ant
                words[i+1]=ant
        if words[i]=='not' and i+2<l and words[i+1]=='a':
            ant=get_antonym(words[i+2])
            if ant !="":
                words[i]=ant
                words[i+2]=ant
    return words


# bag_of_words
def words_to_dict(words):
    return dict([(word, True) for word in words])

def words_to_dict_last_2_letters(words):
    return dict([(word[-2:],True) for word in words])

def remove_stopwords(words):
    english_sw = stopwords.words('english')
    return [word for word in words if word not in english_sw]

#Splits sentence(s) into tokens and removes punctuation marks
def string_tokenize(string):
    tokenizer = WordPunctTokenizer()
    # tokenizer=TreebankWordTokenizer()
    tokens = tokenizer.tokenize(string)
    return [token for token in tokens if token.isalpha()]

def sentence_to_tokens(sentence):
    return remove_stopwords(replace_antonyms(string_tokenize(sentence.lower())))

def trainandclassify(data):
    d=[]
    for s in data:
        l=sentence_to_tokens(s[0])
        d.append((words_to_dict(l),s[1]))
    
    n=len(d)
    sn=[]
    for i in range(n):
        sn.append((d[i][0],d[i][1]))

    classifier=NaiveBayesClassifier.train(sn)
    #classifier.show_most_informative_features()
    return classifier

    '''
    while True:
        s=input()
        d=words_to_dict(sentence_to_tokens(s))
        c=classifier.classify(d)
        print(c)
        
        maxi=0
        for i in range(len(classifier.labels())):
            if c.prob(classifier.labels()[i])>c.prob(classifier.labels()[maxi]):
                maxi=i
        print(classifier.labels()[maxi])
    '''

def main():
    n=int(input())#Number of classes
    l,d,la=[],[],[]
    for i in range(n):
        s=input()
        la.append(s.split(' ',maxsplit=1)[0])
        s=s.split(' ',maxsplit=1)[1]
        l=sentence_to_tokens(s)
        d.append(words_to_dict(l))
    
    train=[]
    for i in range(n):
        sn=[]
        sn.append((d[i],la[i]))
        for j in range(n):
            if j!=i:
                sn.append((d[j],"Not "+la[i]))
        train.append(sn)
    print(train)

    classifiers=[]
    for i in range(n):
        classifiers.append(NaiveBayesClassifier.train(train[i]))

    while True:
        sentence=input()
        d=words_to_dict(sentence_to_tokens(sentence))
        ans=[]
        maxi=0
        for i in range(n):
            ans.append(classifiers[i].prob_classify(d))
            if ans[i].prob(la[i])>ans[maxi].prob(la[maxi]):
                maxi=i
        print(la[maxi])
    

if __name__ == "__main__":
    main()