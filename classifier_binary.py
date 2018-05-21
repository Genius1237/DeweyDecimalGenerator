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

def main():
    negative_sentence1=input()
    """
    negative_sentence1s=sent_tokenize(negative_sentence1)
    print(negative_sentence1s)
    """
    negative_sentence1wclean = sentence_to_tokens(negative_sentence1)

    d = words_to_dict(negative_sentence1wclean)
    l = []
    l.append((d, "neg"))

    positive_sentence1=input()

    positive_sentence1wclean = sentence_to_tokens(positive_sentence1)

    d = words_to_dict(positive_sentence1wclean)
    l.append((d, "pos"))
    
    classifier = NaiveBayesClassifier.train(l)
    while True:
        sentence=input()
        ans=classifier.classify(words_to_dict(sentence_to_tokens(sentence)))
        print(ans)

if __name__ == "__main__":
    main()