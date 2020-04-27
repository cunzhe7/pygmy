import urllib.request


fs = "http://127.0.0.1:35402/"

while True:
     operation = input()
     operation = operation.replace(' ', '%20')
     print(urllib.request.urlopen(fs+operation).read().decode())

