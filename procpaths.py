import os, urllib.request
path = "C:\\Users\\tbmea\\Desktop\\image_gal\\"
paths = []
dates = []
links = []

# with links we run url get and get certain elements
# and fill in descriptions and image credits
html = ""
descs = []
creds = []

for name in os.listdir(path):
	paths.append(path + name)

for path in paths:
	dates.append(os.stat(path).st_mtime)
	try:
		with open(path) as f:
			f.seek(24) # to skip '[InternetShortcut]\nURL='
			links.append(f.read())
	except Exception as err:
		print(err)

for link in links:
	try:
		with urllib.request.urlopen(link) as res:
			html = res.read()
			# find certain elements and get innerhtml and fill descs and creds
	except Exception as err:
		print(err)

# change dates to yyyymmdd
# use dates, descs, creds, and links to build json
# output the json file
# peace out
