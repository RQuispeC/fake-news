all: test-true-en test-fake-en

test-true-en:
	python text_similarity.py -n data/true_01_en.txt -r data/check_01_long_en.txt -t 0.35 -w 0.7
test-fake-en:
	python text_similarity.py -n data/fake_01_en.txt -r data/check_01_long_en.txt -t 0.35 -w 0.7

test-true-por:
	python text_similarity.py -n data/true_01_por.txt -r data/check_01_long_por.txt -t 0.55 -w 0.7 --translate
test-fake-por:
	python text_similarity.py -n data/fake_01_por.txt -r data/check_01_long_por.txt -t 0.55 -w 0.7 --translate
