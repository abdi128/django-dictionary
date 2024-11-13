from django.shortcuts import render
import requests
from PyDictionary import PyDictionary

def index(request):
    return render(request, 'index.html', {})

def word(request):
    search = request.GET.get('search')
    dictionary = PyDictionary()
    meaning = dictionary.meaning(search)
    antonyms_response = requests.get(f'https://api.datamuse.com/words?rel_ant={search}')
    antonyms = [word['word'] for word in antonyms_response.json()]
    synonyms_response = requests.get(f'https://api.datamuse.com/words?rel_syn={search}')
    synonyms = [word['word'] for word in synonyms_response.json()]

    """synonyms = dictionary.synonym(search)
    antonyms = dictionary.antonym(search) """
    if meaning:
        # Flattening the meanings to get the first definition available
        for part_of_speech in meaning.values():
            if part_of_speech:
                first_meaning = part_of_speech[0]
                break

    context = {
        'meaning': first_meaning,
        'antonyms': antonyms,
        'synonyms': synonyms,
        'search': search
    }
    
    return render(request, 'word.html', context)
