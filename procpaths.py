## EXTRACT DATA FROM INTERNET SHORTCUT FILES AND URL ASSOCIATED W/EACH
## BY DEFAULT EACH URL IS ASSUMED TO BE A BING.COM SPOTLIGHT QUERY
import os, time, urllib.request


# first collect last-modified timestamps and URLs contained in file
dates = []
links = []
t = time.localtime()
mo = ''
dd = ''
hh = ''
mm = ''
ss = ''
def pad(x):
	return ('0' if x < 10 else '') + repr(x)


## MUST RUN IN DIRECTORY WITH INTERNET SHORTCUTS TO PROCESS
for name in os.listdir('.'):
	t = time.localtime(os.stat(name).st_mtime)
	mo = pad(t.tm_mon)
	dd = pad(t.tm_mday)
	hh = pad(t.tm_hour)
	mm = pad(t.tm_min)
	ss = pad(t.tm_sec)
	dates.append(repr(t.tm_year) + mo + dd + hh + mm + ss)
	try:
		with open(name) as file:
			file.seek(24) # to skip '[InternetShortcut]\nURL='
			links.append(file.read())
	except Exception as err:
		print(err)


# with links we run url get and get certain elements to fill in 
# [by default] location descriptions and image credits
err_msg = ''
FAIL_MSG = "recorded in place of each data point for entry"
i_err = -1
NOT_SPOT = "Not a Bing search spotlight"
html = ""
DESC_ID = 'id="heading-url">'
tmp = -1
DES_ALT = 'class="text-location">'
CRED_CL = 'class="copyright-text">'
CLOSE_DIV = '</div>'
i_tc0 = -1
i_tclen = -1
tc = ''
descs = []
creds = []


# HTMLParser would be ideal but can't get it to work right now
for link in links:
	if link.find('spotlight') < 0:
		descs.append(NOT_SPOT)
		creds.append(NOT_SPOT)
	else: 
		try:
			with urllib.request.urlopen(link) as res:
				html = repr(res.read())
				tmp = html.find(DESC_ID)
				i_tc0 = html.find(DES_ALT if tmp < 0 else DESC_ID)
				i_tc0 += len(DES_ALT if tmp < 0 else DESC_ID)
				i_tclen = i_tc0 + html[i_tc0:].find(CLOSE_DIV)
				descs.append(html[i_tc0:i_tclen])
				i_tc0 = html.find(CRED_CL) + len(CRED_CL)
				i_tclen = i_tc0 + html[i_tc0:].find(CLOSE_DIV)
				creds.append(html[i_tc0:i_tclen])
		except Exception as err:
			err_msg = repr(err)
			descs.append(err_msg)
			creds.append(err_msg)
			i_err = repr(links.index(link))
			print(' '.join([err_msg, FAIL_MSG, i_err]))


# OUTPUT SQL TABLE ENTRY DATA
OPEN = '('
CONT = ',\n('
DLIM = '",\n\t"'
CLOS = '"\n)'
def sqlwrap(*data, is_cont=True):
	return (CONT if is_cont else OPEN) + DLIM[2:] + DLIM.join(*data) + CLOS

try:
	with open('data.txt', 'a', encoding="utf-8") as file:
		for i in range(len(dates)):
			file.write(sqlwrap([dates[i], descs[i], creds[i], links[i]]))
except Exception as err:
		print(err)

