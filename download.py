from requests_oauthlib import *
from requests import *
from commands import *

client_id = "f2bc5aa04a184895b0712ce8b7d622fa"
client_secret = "bd146cb950f6444bbcedbcf28bfe9c91"
auth_url = "https://oauth.yandex.ru/authorize"
token_url = "https://oauth.yandex.ru/token"

filename = download_window()

oauth = OAuth2Session(client_id=client_id)
authorization_url, state = oauth.authorization_url(auth_url, force_confirm="true")

print("Перейдите по ссылке, авторизуйтесь и скопируйте код:", authorization_url)
code = input("Вставьте одноразовый код: ")

token = oauth.fetch_token(token_url=token_url,
                          code=code,
                          client_secret=client_secret)
access_token = token["access_token"]

headers = {"Authorization": f"OAuth {access_token}"}
params = {"path": filename}
r = get("https://cloud-api.yandex.net/v1/disk/resources/download", headers=headers, params=params)

download_url = r.json()['href']
download_response = get(download_url, stream=True)
if download_response.status_code == 200:
    filename = params['path']
    with open(filename, 'wb') as f:
        for chunk in download_response.iter_content(chunk_size=8192):
            f.write(chunk)
    print(f"Файл '{filename}' успешно скачан.")
else:
    print(f"Ошибка при скачивании файла. Код статуса: {download_response.status_code}")
    print(download_response.text)
