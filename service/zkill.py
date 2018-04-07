from cache import cache

import requests

import killmail

#takes in a list of character.Characters
#returns a list of killmail.Killmail
@cache(time=5)
def get_character_killmails(characters):
    mails = []

    #zkillboard requires the ids to be sorted for its api
    character_ids = []
    for character in characters:
        character_ids.append(character.id)
    character_ids.sort()

    character_id_str = ",".join(str(i) for i in character_ids)
    url = "https://zkillboard.com/api/characterID/" + character_id_str + "/"
    headers = {'Accept-Encoding': 'gzip', 'User-Agent': 'naabers'}
    search_results = requests.get(url, headers=headers)
    raw_mails = search_results.json()

    for raw_mail in raw_mails:
        mails.append(killmail.Killmail(raw_mail))

    return mails