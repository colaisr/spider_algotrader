import urllib
from urllib.request import urlopen

#server_url = "http://127.0.0.1:5000/"
server_url = "http://colak.eu.pythonanywhere.com/"

print("*****updating FGI for today")
url = server_url + "research/updatefgiscore"
response = urllib.request.urlopen(url)
print("**** Done *****")

