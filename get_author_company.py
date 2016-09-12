#!/usr/bin/python3

import os
import re
import sys


# domain: (companyName, priority)
companies = {
	'owncloud.com': ('ownCloud', 1),
	'owncloud.org': ('ownCloud', 1),
	'solidgear.es': ('ownCloud', 1),
	'butonic.de': ('ownCloud', 1),
	'tmit.eu': ('ownCloud', 1),
	'nextcloud.com': ('Nextcloud', 2),
}

multipleEmails = [
	re.match(r'.* \<([^>]+)\> .* \<([^>]+)\>', line)
	for line in open('/home/robin/.mailmap').read().splitlines()
	if line.count('@') > 1
]

mailMap = [
	(match.group(1), match.group(2))
	for match in multipleEmails
]

def normalizeMail(mail):
	mailPairs = [
		pair for pair in mailMap
		if pair[1] == mail
	]
	if len(mailPairs):
		return mailPairs[0][0]
	else:
		return mail;

def getAllMails(mail):
	normalized = normalizeMail(mail)
	alternativeMails = [
		pair[1] for pair in mailMap
		if pair[0] == normalized
	]
	
	return [normalized] + alternativeMails

def getCompany(domains):
	matchedCompany = ''
	matchedPriority = 0
	for domain, (company, priority) in companies.items():
		if (domain in domains and priority > matchedPriority):
			matchedPriority = priority
			matchedCompany = company
	return matchedCompany

inputMail = sys.argv[1]
if ('-bot@' in inputMail or 'bot@nextcloud.com' == inputMail):
	print('Bot')
else:
	if (len(inputMail.split('@'))>1):
		inputDomain = inputMail.split('@')[1];
	else:
		inputDomain = inputMail;
	# first check for the commit mail
	company = getCompany([inputDomain]);
	if (company):
		print(company)
	else:
		# then check aliases
		allMails = getAllMails(inputMail)
		domains = set([
			mail.split('@')[1]
			for mail in allMails
		])

		company = getCompany(domains);
		if (company):
			print(company)
		else:
			print("Other")
