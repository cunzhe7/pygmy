import urllib.request

fs = "http://elnux1.cs.umass.edu:35400/update/1/10/"

print(urllib.request.urlopen(fs).read().decode())