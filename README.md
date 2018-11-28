# SEMANTIC SIMILARITY FOR FAKE NEWS DETECTION

This repo implements a semantic similarity method using YAGO, DBpedia and WordNet.

This method is tested for authomatic fake detection.

## Prerequisites:

* python 2
* nltk
* [sematch](https://github.com/gsi-upm/sematch)

In case you want to test news in portuguese you will need package `dict`.

## Run demo

```bash
git clone https://github.com/RQuispeC/fake-news.git
cd fake-news
make
```

Main source code is `text_similarity.py`. Available flags are:
```
-n , --news  path for archive of evaluated news.
-r , --reference path for archive of reference news.
-t , --threshold threshold used to determinated is news is fake or not.
-w , --weight weigth used for DBpedia similarity score over WordNet similarity.
-s {path,lin,lch}, --similarity {path,lin,lch} similarity metric used, default 'path'.
--translate           Whether or not to translate input data.
--debug               Print debug messages.
```

You can find other examples of flags use in `Makefile`.

This work was presented as a project for the course of Databases dictated by [Julio Cesar dos Reis](http://ic.unicamp.br/~jreis/) at University of Campinas in fall 2018.

Questions? Don't hesitate to contact the author [Rodolfo Quispe](https://github.com/RQuispeC) 
