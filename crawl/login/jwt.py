import requests
from urllib.parse import urljoin

BASE_URL='https://login3.scrape.center/'
login_url=urljoin(BASE_URL, '/api/login')
index_url=urljoin(BASE_URL,'/api/book')

USERNAME='admin'
PASSWORD='admin'

response_login=requests.post(login_url,json={'username':USERNAME,'password':PASSWORD})
print('login status code:',response_login.status_code)
data=response_login.json()
print('login data:',data['token'])

token=data['token']
headers={'Authorization':'jwt '+token}
response_index=requests.get(index_url,headers=headers,params={
    'limit':18,
    'offset':0
})
print(response_index.status_code)
print(response_index.url)
print(response_index.json())