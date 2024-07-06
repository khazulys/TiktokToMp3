import requests
import os

def TikTok_to_Mp3(tiktok_url):
  url = "https://tiktok-scraper7.p.rapidapi.com/"
  data = {"url":tiktok_url,"hd":"1"}
  headers = {
	    "x-rapidapi-key": "4633877495msh33a460d911384a3p1e63fdjsnd7724771fb4d",
	    "x-rapidapi-host": "tiktok-scraper7.p.rapidapi.com"}
  response = requests.get(url, headers=headers, params=data)
  audio_url = response.json().get("data")["music"]
  filename = os.path.basename(audio_url)
  #print(filename)
  
  #Menyimpan audio
  
  audio_response = requests.get(audio_url).content
  
  with open(filename,"wb") as file:
    file.write(audio_response)
  
  return filename
  #print(f"Succes convert Tiktok Video to Mp3. Saved as {filename} ")
#TikTok_to_Mp3("https://vm.tiktok.com/ZSYXRJdkV/")