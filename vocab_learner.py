from main import get_tokens, get_tokens_by_line, TokenType
from collections import Counter, defaultdict




def divide_lemmas(upper, lower, lemmas):
    known = set()
    unknown = defaultdict(list)
    for w, count in lemmas.most_common():
        if count >= upper:
            known.add(w)
        elif count > lower:
            unknown[count].append(w)
    return known, unknown


def score_sentences(sents, known, target):
    score = dict()
    for key, words in sents.items():
        if target in words: 
            score[key] = len([word for word in words if word in known]) / len(words)
    return sorted(score.items(), key=lambda x: x[1], reverse=True)


def get_sentences_for_word(sentences, known, word, number_of_occurrences):
    scores = score_sentences(sentences, known, word)
    known.add(word)
    return sorted(scores, key=lambda x: x[0])[0:number_of_occurrences]

def learn_vocab(knwon, unknown, occurs, sents_lemmas, sents_text, ofile, ref_prettifier=lambda x: x):
    

    with open(ofile, 'w', encoding="UTF-8") as f:

        while len(unknown.keys()) > 0:
            current_key = max(unknown.keys())
            current = unknown[current_key]
            print("Item frequency ", current_key, ". Total Items: ", len(current), file=f)
            for w in current:
                verses = get_sentences_for_word(sents_lemmas, KNOWN, w, occurs)
                print(w, file=f)
                for verse in verses:
                    print(ref_prettifier(verse[0]),  '-', ' '.join(sents_text[verse[0]]), file=f)
                print('', file=f)
            del unknown[current_key]
            print('', file=f)
    print("DONE!")

UPPER_LIMIT = 125 
LOWER_LIMIT = 100
OCCURRENCES  = 5


LEMMAS = Counter(get_tokens(TokenType.lemma))
SENTS = get_tokens_by_line(TokenType.lemma)
SENTS_TEXT = get_tokens_by_line(TokenType.text)


REF_CLEANER = lambda x: bcv_to_verse_ref(x, start=61)

KNOWN, UNKNOWN = divide_lemmas(UPPER_LIMIT, LOWER_LIMIT, LEMMAS)

learn_vocab(KNOWN, UNKNOWN, OCCURRENCES, SENTS, SENTS_TEXT, "list_to_learn.txt")
