import os

def format_dict_translation(t_string, word):
  t_string = t_string[t_string.find(word) + len(word) + 1:].strip() #ger only translations
  items = t_string.split("\n")
  translations = []
  for i in items:
    i = i[i.find(".") + 1:].strip() #remove numeration
    i = i.split(";") # multiple translation with same relevance
    for w in i:
      translations.append(w.strip())
  return translations
  
def translate(words):
  translated_words = []
  for word in words:
    try:
      translation = os.popen('dict -d fd-por-eng --nocorrect  ' + word + " 2> /dev/null").read()
      translation_list = format_dict_translation(translation, word)
      translated_words.append(translation_list)
    except ValueError:
      pass
  return translated_words

