import requests

from .cache import cache
from . import killmail


#takes in a map of character ids to names
#returns a list of killmail.Killmail
@cache(time=5)
def get_character_killmails(character_id_map):
    mails = []

    for character in character_id_map:
        url = "https://zkillboard.com/api/characterID/" + str(character) + "/"
        headers = {'Accept-Encoding': 'gzip', 'User-Agent': 'naabers'}
        search_results = requests.get(url, headers=headers)
        raw_mails = search_results.json()

        for raw_mail in raw_mails:
            mails.append(killmail.Killmail(raw_mail))

    return mails