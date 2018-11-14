import nltk
from nltk.corpus import wordnet as wn

def word_similarity(word, text, metric = 'distance'):
    max_sim = 0
    wordnet_set = wn.synsets(word)
    if len(wordnet_set) == 0:
        #print('Warning: word {} has not match in wordnet'.format(word))
        return 0
    word_wn= wordnet_set[0] #in the meantime we consider the first match
    best_match = ''
    for t in text:
        wordnet_set = wn.synsets(t)
        if len(wordnet_set) == 0:
            continue
        other = wordnet_set[0]
        try:
            if metric == 'distance':
                sim = word_wn.path_similarity(other)
               # print('{} and {} has similarity {}'.format(word, t, sim))
                if sim != None  and sim > max_sim:
                    max_sim = sim
                    best_match = t
        except ValueError:
            pass
    #print('Best similarity for word {} is {} and score {:.4f}'.format(word, best_match, max_sim))
    return max_sim

def text_similarity(text_1, text_2):
    text_1 = nltk.word_tokenize(text_1)
    text_2 = nltk.word_tokenize(text_2)
    score = 0 
    for t in text_1:
        score += word_similarity(t, text_2)
    for t in text_2:
        score += word_similarity(t, text_1)
    return score

def read_file(path):
    text = open(path)
    str_text = ""
    for line in text:
        str_text += line + "\n"
    return str_text

if __name__ == '__main__':
 
    fake = read_file('fake_01_en.txt')
    true = read_file('true_01_en.txt')
    check = read_file('check_01_01_en.txt')
    
    score = text_similarity(fake, check)
    print('Fake score is {:.4f}'.format(score))
   
    score = text_similarity(true, check)
    print('True score is {:.4f}'.format(score))
   
   
