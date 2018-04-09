import multiprocessing
import requests

from .cache import cache
from . import killmail


#takes in a map of character ids to names
#returns a list of killmail.Killmail
def get_characters_killmails(character_id_map):
    mails = []
    character_ids = list(character_id_map)

    pool = multiprocessing.Pool(processes=10)
    raw_mail_list_of_lists = pool.map(multiprocessing_get_killmails,
                                      character_ids)
    pool.close()
    pool.join()

    for raw_mails in raw_mail_list_of_lists:
        for raw_mail in raw_mails:
            mails.append(killmail.Killmail(raw_mail))

    return mails

def multiprocessing_get_killmails(character_id):
    return get_character_killmails(character_id)

#takes in a character ids
#returns a list of raw json killmails
@cache(time=5)
def get_character_killmails(character_id):
    url = "https://zkillboard.com/api/characterID/" + str(character_id) + "/limit/100/"
    headers = {'Accept-Encoding': 'gzip', 'User-Agent': 'naabers'}
    search_results = requests.get(url, headers=headers)
    raw_mails = search_results.json()

    return raw_mails