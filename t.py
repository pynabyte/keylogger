import requests,json

url = "https://www.virustotal.com/api/v3/files"

# files = { "file": ("malware.apk", open("malware.apk", "rb"), "application/x-gsarcade-usersvc") } # for apk files
files = { "file": ("rufus-4.4.exe", open("rufus-4.4.exe", "rb"), "application/x-msdownload") } # for exe files
headers = {
    "accept": "application/json",
    "x-apikey": "c1d10849f714fe159dce979ea875c0893c9345109b4c3463964f65f744a19979",
}

response = requests.post(url, files=files, headers=headers)

# print(response.text)

# analysis_id = json.loads(response.text)['data']['id']
# print(analysis_id)
# analysis_url = f"https://www.virustotal.com/api/v3/analyses/{analysis_id}"


response2 = requests.get(json.loads(response.text)['data']['links']['self'], headers=headers)

print(json.loads(response2.text)['data']['attributes']['status'])
print(json.loads(response2.text)['data']['attributes']['stats']['malicious'])