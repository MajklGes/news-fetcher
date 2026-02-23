import requests

url = "https://ncxcpeeocknrotbzmfde.supabase.co/rest/v1/articles?select=*"

headers = {
    "apikey": "sb_publishable_L1AIP3X0SS5_-S5SbX0M7Q_KMWjfCLj",
    "Authorization": "Bearer sb_publishable_L1AIP3X0SS5_-S5SbX0M7Q_KMWjfCLj"
}

response = requests.get(url, headers=headers)

print(response.status_code)
print(response.text)