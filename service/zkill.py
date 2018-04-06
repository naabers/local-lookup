import requests

import killmail

#takes in a list of character.Characters
#returns a list of killmail.Killmail
def get_character_losses(characters):
    killmails = []

    #zkillboard requires the ids to be sorted for its api
    character_ids = []
    for character in characters:
        character_ids.append(character.id)
    character_ids.sort()

    character_id_str = ",".join(str(i) for i in character_ids)
    url = "https://zkillboard.com/api/losses/characterID/" + character_id_str + "/"
    headers = {'Accept-Encoding': 'gzip', 'User-Agent': 'naabers'}
    search_results = requests.get(url, headers=headers)
    raw_lossmails = search_results.json()

    for raw_lossmail in raw_lossmails:
        killmails.append(killmail.Killmail(raw_lossmail))

    return killmails
