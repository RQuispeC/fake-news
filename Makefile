all: true-en-1 fake-en-1

true-en-1:
	python text_similarity.py -n data/true_01_en.txt -r data/check_01_long_en.txt -t 0.36 -w 0.7
fake-en-1:
	python text_similarity.py -n data/fake_01_en.txt -r data/check_01_long_en.txt -t 0.36 -w 0.7
true-por-1:
	python text_similarity.py -n data/true_01_por.txt -r data/check_01_long_por.txt -t 0.55 -w 0.7 --translate
fake-por-1:
	python text_similarity.py -n data/fake_01_por.txt -r data/check_01_long_por.txt -t 0.55 -w 0.7 --translate

true-en-2:
	python text_similarity.py -n data/true_02_en.txt -r data/check_02_long_en.txt -t 0.36 -w 0.7
fake-en-2:
	python text_similarity.py -n data/fake_02_en.txt -r data/check_02_long_en.txt -t 0.36 -w 0.7
true-por-2:
	python text_similarity.py -n data/true_02_por.txt -r data/check_02_long_por.txt -t 0.55 -w 0.7 --translate
fake-por-2:
	python text_similarity.py -n data/fake_02_por.txt -r data/check_02_long_por.txt -t 0.55 -w 0.7 --translate

hard-test-en:
	python text_similarity.py -n data/text_00_en.txt -r data/text_01_en.txt -t 0.36 -w 0.7
hard-test-por:
	python text_similarity.py -n data/text_00_por.txt -r data/text_01_por.txt -t 0.55 -w 0.7 --translate
