import nltk
from nltk.corpus import wordnet as wn

def word_similarity(word, text, metric = 'distance'):
    max_sim = 0
    wordnet_set = wn.synsets(word)
    if len(wordnet_set) == 0:
        #print('Warning: word {} has not match in wordnet'.format(word))
        return 0, False
    word_wn= wordnet_set[0] #in the meantime we consider the first match
    best_match = ''
    ok = False
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
                    ok = True
        except ValueError:
            pass
    #print('Best similarity for word {} is {} and score {:.4f}'.format(word, best_match, max_sim))
    return max_sim, ok

def text_similarity(text_1, text_2):
    text_1 = nltk.word_tokenize(text_1)
    text_2 = nltk.word_tokenize(text_2)
    text_1 = list(set(text_1))
    text_2 = list(set(text_2))
    score = 0 
    cnt = 0
    for t in text_1:
        score_w, ok = word_similarity(t, text_2)
        if ok:
            score += score_w
            cnt += 1
    for t in text_2:
        score_w, ok = word_similarity(t, text_1)
        if ok:
            score += score_w
            cnt += 1
    return score/cnt

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
   
   
