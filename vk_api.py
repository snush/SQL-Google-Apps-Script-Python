import requests

access_token = '74803d2274803d2274803d22e674fd528d7748074803d22165319cf5938311c3180110a'
api_version = '5.92'

images = []
vk_wall = requests.get(f'https://api.vk.com/method/photos.get?owner_id=-2344658&album_id=wall&access_token={access_token}&v={api_version}')

for i in range(1, len(vk_wall.json()['response']['items'])):
  images.append(vk_wall.json()['response']['items'][i]['sizes'][4]['url'])

with open("vk.texts.txt", "wt", encoding = "utf8") as f:
    for link in images:
        f.write(link.replace("\n", " ") + "\n")
        print(link.replace("\n", " "))
      