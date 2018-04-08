import requests

from .cache import cache
from . import killmail


#takes in a map of character ids to names
#returns a list of killmail.Killmail
@cache(time=5)
def get_character_killmails(character_id_map):
    mails = []

    #zkillboard requires the ids to be sorted for its api
    character_ids = list(character_id_map)
    character_ids.sort()

    character_id_str = ",".join(str(i) for i in character_ids)
    url = "https://zkillboard.com/api/characterID/" + character_id_str + "/"
    headers = {'Accept-Encoding': 'gzip', 'User-Agent': 'naabers'}
    search_results = requests.get(url, headers=headers)
    raw_mails = search_results.json()

    for raw_mail in raw_mails:
        mails.append(killmail.Killmail(raw_mail))

    return mails