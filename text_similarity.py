import argparse
import re
import ipdb

import nltk
from nltk.corpus import wordnet as wn
from nltk.tokenize import TweetTokenizer

from translation import translate

from sematch.application import Matcher
from sematch.semantic.graph import DBpediaDataTransform, Taxonomy
from sematch.semantic.similarity import WordNetSimilarity, YagoTypeSimilarity, ConceptSimilarity 

parser = argparse.ArgumentParser(description='Parameters for semantic similarity based on ontologies')
# news and reference path
parser.add_argument('-n', '--news', type=str, help="path for archive of evaluated news in portuguese")
parser.add_argument('-r', '--reference', type=str, help="path for archive of reference news in portuguese")
parser.add_argument('-t', '--threshold', type=float, default = 0.35, help="threshold used to determinated is news is fake or not")
parser.add_argument('-w', '--weight', type=float, default = 0.5, help="weigth used for DBpedia similarity score over WordNet similarity")
parser.add_argument('-s', '--similarity', default='path', type=str, choices=['path', 'lin', 'lch'], help="similarity metric used, default 'path'")
parser.add_argument('--translate', action='store_true', help="Whether or not to translate input data")
parser.add_argument('--debug', action='store_true', help="Print debug messages")
args = parser.parse_args()

matcher = Matcher()
wns = WordNetSimilarity()
concept = ConceptSimilarity(Taxonomy(DBpediaDataTransform()), 'models/dbpedia_type_ic.txt')
yago_sim = YagoTypeSimilarity()

def clean_text(text):
    tknzr = TweetTokenizer(strip_handles=True, reduce_len=True)
    text = tknzr.tokenize(text)
    text = list(set(text))
    clean_text = []
    for word in text:
       if re.search('[a-zA-Z]', word):
           clean_text.append(word)
    return clean_text

def get_dbpedia_id(type_dict):
    if not 'lod' in type_dict:
        return None
    for item in type_dict['lod']:
        #if item.find('dbpedia.org/ontology/') >= 0:
        if item.find('dbpedia.org/class/yago/') >= 0:
            return item
    return None


def get_yago_id(type_dict):
    if not 'lod' in type_dict:
        return None
    for item in type_dict['lod']:
        if item.find('dbpedia.org/class/yago/') >= 0:
            return item
    return None

def is_ascii(s):
    return all(ord(c) < 128 for c in s)

def word_similarity(word_list, text_list):
    """
    Computes the similarity between word and text

    word_list: a list containing all possible translations of a single word
    text_list: a list of lists containing all possible translations for a set of words  
    """

    max_sim_wordnet = 0
    max_sim_dbpedia = 0
    ok_wordnet = False
    ok_dbpedia = False
    for word in word_list:
        if not is_ascii(word):
            continue
        type_word = matcher.type_links(word)
        if len(type_word) == 0: #there is not match of word in knowledge graphs
            continue

        type_word = type_word[0]#use only fist match
        w_dbpedia_id = get_dbpedia_id(type_word)

        for l in text_list:
            for other in l:
                try:
                    sim = wns.word_similarity(word, other, args.similarity)
                    if sim and sim > max_sim_wordnet:
                        max_sim_wordnet = sim
                        ok_wordnet = True

                    if w_dbpedia_id == None:
                        continue
                    type_word = matcher.type_links(other)
                    if len(type_word) == 0: #there is not match for other in knowledge graph
                        continue

                    type_word = type_word[0]#use only fist match
                    o_dbpedia_id = get_dbpedia_id(type_word)
                    if o_dbpedia_id == None:
                        continue
                    #sim = concept.similarity(w_dbpedia_id, o_dbpedia_id, args.similarity)
                    sim = yago_sim.yago_similarity(w_dbpedia_id, o_dbpedia_id, args.similarity)
                    if sim and sim > max_sim_dbpedia:
                        max_sim_dbpedia = sim
                        ok_dbpedia = True

                except ValueError:
                    pass
    return max_sim_wordnet, max_sim_dbpedia, ok_wordnet, ok_dbpedia

def text_similarity(text_1, text_2):
    #tokenize, get unique words and clean data.
    text_1 = clean_text(text_1)
    text_2 = clean_text(text_2)

    #word-to-word translation
    if args.translate:
        print("Translating data")
        text_1 = translate(text_1)
        text_2 = translate(text_2)
    else:
        print("Text already in english")
        text_1 = [[word] for word in text_1] #convert in an list of list
        text_2 = [[word] for word in text_2] #convert in an list of list

    score_wordnet = 0
    score_dbpedia = 0 
    cnt_wordnet = 0
    cnt_dbpedia = 0
    if args.debug:
        print(len(text_1),len(text_2))
    for xx, t in enumerate(text_1):
        if args.debug:
            print('-->', xx, t)
        score_wordnet_r, score_dbpedia_r, ok_wordnet, ok_dbpedia = word_similarity(t, text_2)
        if ok_wordnet:
            if args.debug:
                print("++", cnt_wordnet)
            score_wordnet += score_wordnet_r
            cnt_wordnet += 1
        if ok_dbpedia:
            if args.debug:
                print("--", cnt_dbpedia)
            score_dbpedia += score_dbpedia_r
            cnt_dbpedia += 1
    if args.debug:
        print("Done with text 1")

    for xx, t in enumerate(text_2):
        if args.debug:
            print('-->', xx, t)
        score_wordnet_r, score_dbpedia_r, ok_wordnet, ok_dbpedia = word_similarity(t, text_1)
        if ok_wordnet:
            if args.debug:
                print("++", cnt_wordnet)
            score_wordnet += score_wordnet_r
            cnt_wordnet += 1
        if ok_dbpedia:
            if args.debug:
                print("--", cnt_dbpedia)
            score_dbpedia += score_dbpedia_r
            cnt_dbpedia += 1
    if args.debug:
        print("Done with text 2")

    if cnt_wordnet != 0:
        score_wordnet /= cnt_wordnet
    if cnt_dbpedia != 0:
        score_dbpedia /= cnt_dbpedia
    return score_wordnet, score_dbpedia

def read_file(path):
    text = open(path)
    str_text = ""
    for line in text:
        str_text += line + "\n"
    return str_text

def main():
    news = read_file(args.news)
    reference = read_file(args.reference)
    threshold = args.threshold

    score_wordnet, score_dbpedia = text_similarity(news, reference)
    score = score_dbpedia*args.weight + (1. - args.weight)*score_wordnet
    print("======================================================= ")
    print("===FAKE NEWS DETECTION BASED ON SEMANTIC SIMILARITY==== ")
    print("======================================================= ")
    print("NEWS=================================================== ")
    print(news)
    print("REFERENCE============================================== ")
    print(reference)
    print("======================================================= ")
    print("Similarity Score DBpedia: {:.4f}".format(score_dbpedia))
    print("Similarity Score WordNet: {:.4f}".format(score_wordnet))
    print("Similarity Score: {:.4f}*{:.2f} + {:.4f}*{:.2f} = {:.4f}".format(score_dbpedia, args.weight,score_wordnet, 1. - args.weight, score))
    print("News {} fake!".format("is" if score < threshold else "is not"))
if __name__ == '__main__':
   main()
   
