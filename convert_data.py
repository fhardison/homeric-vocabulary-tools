from pathlib import Path
from lxml import etree
from collections import defaultdict


iliad  = (Path('./source_data/texts/tlg0012.tlg001.perseus-grc1.tb.xml'), './texts/iliad.txt')
odd = (Path('./source_data/texts/tlg0012.tlg002.perseus-grc1.tb.xml'), './texts/odyssey.txt')

def convert(datapath, book_path):
    dom = etree.parse(datapath)
    BOOK = 0
    CURBOOK = 0
    PUNCT = 'u--------'



    with open(Path(book_path), 'w', encoding="UTF-8") as f:
        sentences = dom.findall('.//sentence')
        sent_num = 0
        data = defaultdict(dict)
        for sent in sentences:
            newbook = int(sent.get('subdoc').split('.')[0])
            if newbook != CURBOOK:
                CURBOOK = newbook
                sent_num = 0
                BOOK = CURBOOK
            sent_num += 1
            words = defaultdict(list)
            lemmas = defaultdict(list)
            parses = defaultdict(list)
            text = defaultdict(list)
            start_quote = ''
            for word in sent.findall('.//word'):
                form = word.get('form')
                if '[' in form and ']' in form:
                    continue
                lemma = word.get('lemma')
                parse = word.get('postag')
                cite = word.get('cite')
                
                if parse != PUNCT:
                    if cite:
                        line_num = int(cite.split(':')[-1].split('.')[-1])
                if not form:
                    print(f'Error on {sent_num}')
                    continue
                
                if parse == PUNCT:
                    try:
                        if len(text[line_num]) == 0 and (form == '"' or form == '̓"̓'):
                            start_quote = '"'
                        elif len(text[line_num]) == 0 and form == "̓":
                            start_quote = "̓" 
                        elif form == '':
                            continue
                        else:
                            text[line_num][-1] = text[line_num][-1].strip() + form
                    except Exception as e:
                        print(word)
                        print(sent.get('subdoc'))
                        print(newbook, line_num, form, word.get('id'))
                        print(e)
                        exit()
                    continue
                if start_quote != '':
                    text[line_num].append(start_quote + form)
                    start_quote = ''
                else:
                    text[line_num].append(form)
                words[line_num].append(form)
                lemmas[line_num].append(lemma or '.')
                parses[line_num].append(parse or '.')
            data[BOOK][sent_num] = (text, words, lemmas, parses)
        for book, sentences in sorted(data.items(), key=lambda x: int(f"{x[0]:02}")):
            for key, (text, words, lemmas, parses) in sorted(sentences.items(), key=lambda x: int(f"{x[0]:03}")):
                for line_num, line_text in sorted(text.items(), key=lambda x: int(f"{x[0]:3}")):
                    if len(line_text) < 1:
                        continue
                    print(f'{book}.{key}.{line_num}')
                    print(f'{book:02}.{key:03}.{line_num:03}.text', ' '.join(line_text), file=f)
                    print(f'{book:02}.{key:03}.{line_num:03}.form', ' '.join(words[line_num]), file=f)
                    print(f'{book:02}.{key:03}.{line_num:03}.lemma', ' '.join(lemmas[line_num]), file=f)
                    print(f'{book:02}.{key:03}.{line_num:03}.parse', ' '.join(parses[line_num]), file=f)
                    print('', file=f)
                    
convert(iliad[0], iliad[1])
convert(odd[0], odd[1])
