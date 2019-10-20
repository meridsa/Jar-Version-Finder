#!/usr/local/bin/python3
""" 
	Python script takes in an option and an arguemnt (the filename containing
	the checksums and jar names) and searches the checksums in an online repo
	to find the version number

	Note all comments explain the purpose of the lines of code underneath
	if the comment has a hash (#) on both sides the functionality described has
	been implemented

	Version 2.0: Using only python script
"""

#------- IN TESTING AND EARLY DEV STAGE

# import statements
import requests
from datetime import datetime
import pandas as pd
import sys, argparse
import os
import hashlib
from pathlib import Path

def findSha1sumHash(jarfilename):
	"""Hashes files with sha 1 sum and returns it"""
	BLOCKSIZE = 65565
	hasher = hashlib.sha1()
	with open(jarfilename, 'rb') as afile:
		try:
			buf = afile.read(BLOCKSIZE)
			while len(buf) > 0:
				hasher.update(buf)
				buf = afile.read(BLOCKSIZE)
		except:
			print('{} too large, cannot hash so will be empty in final csv\n'.format(jarfilename))
			return '0'*40
	return str(hasher.hexdigest())

def findWantedFilesInDirectory(directory, wantedFileTypes=['.jar', '.ear', '.war']):
	"""Finds all wanted file types in a directory and makes a list of dictionaries with their names and sha 1 sums"""
	fileAndSha1sumDict = []
	for file in os.listdir(directory):
		for wantedFileType in wantedFileTypes:
			if file.endswith(wantedFileType):
				sha1sum = findSha1sumHash(file)
				fileAndSha1sumDict.append({'File': file, 'sha1sum': sha1sum})
	return fileAndSha1sumDict


def checkSha1sumAgainstRepo(sha1sum):
	"""checks maven central for sha1sum, if not found returns dict with not found as all values"""
	urlString = "https://search.maven.org/solrsearch/select?q=1:\"{}\"&rows=20&wt=json".format(str(sha1sum))
	resp = requests.get(urlString)
	json_data = resp.json()
	if json_data['response']['numFound'] == 0:
		# This means something went wrong.
		return {"groupId": "not found",
			"artifactId": "not found",
			"version": "not found",
			"filetype": "not found",
			"date uploaded": "not found"}
	docs = json_data['response']['docs'][0]
	groupId = docs['g']
	artifactId = docs['a']
	version = docs['v']
	filetype = docs['p']
	timestamp = docs['timestamp']/1000
	# convert timestamp into date format month-year
	date = datetime.fromtimestamp(timestamp) 
	dateString = date.strftime("%M-%Y")
	return {"groupId": groupId,
		"artifactId": artifactId,
		"version": version,
		"filetype": filetype,
		"date uploaded": dateString}


def concatDictsInDataFrame(rawDataList, collectedDataList):
	finalCorrectlyFormatedListOfDicts = []
	for collectedData, rawData in zip(collectedDataList, rawDataList):
		finalCorrectlyFormatedListOfDicts.append({
			'File': rawData['File'],
			'groupId': collectedData['groupId'],
			'artifactId': collectedData['artifactId'],
			'version': collectedData['version'],
			'Release Date': collectedData['date uploaded'],
			'sha1sum': rawData['sha1sum']
			})
	return finalCorrectlyFormatedListOfDicts

def main(argv):
	targetDirectory = os.getcwd()
	recursiveDepth=1
	test = True
	# no options is only current directory
	# -t is test, uses target directory (either current or directed with -d) shows result and deletes the contents after running
	# -r is recursive, number after shows max depth, if omitted recursive depth is set to 10
	# -d targets a directory, followed by directory path, if omitted fails
	# -h is help
	listRawData = findWantedFilesInDirectory(targetDirectory)
	listFoundDictData = []
	for dictRawData in listRawData:
		listFoundDictData.append(checkSha1sumAgainstRepo(dictRawData['sha1sum']))
	resultList = concatDictsInDataFrame(listRawData, listFoundDictData)
	dfResult = pd.DataFrame(resultList)
	if test:
		print(dfResult.head())
	else:
		# save pandas dataframe to a csv that you can name
		defaultFileName = "jarInFolderInformation"
		filename = str(input("What do you want to call this csv? Default=[{}]; .csv extention not needed\n".format(defaultFileName)))
		filename = filename + ".csv"
		with open(filename, "w+") as outFile:
			dfResult.to_csv(filename, sep="\t")


	


if __name__ == "__main__":
	main(sys.argv)




""" 
	Maven central repo:
	These URLs allow you to access the search functionality of the Central 
	Repository from any non-browser user agent. Note that the "wt" parameter 
	present in every URL determines the format of the results. Setting "wt" 
	equal to "json" will provide a JSON response, while setting "wt" equal 
	to "xml" will provide the same response formatted as an XML document. 
	Another common parameter is "rows," which limits the number of results 
	returned by the server.

	NOTE: Most of the URLs in this document have been URL-decoded for the 
	sake of readability. They should work when pasted into a web browser, 
	but you may have to URL-encode them to function when called 
	programmatically.
	
	org.eclipse.jetty:jetty-webapp:7.3.0.v20110203 = 35379fb6526fd019f331542b4e9ae2e566c57933

	ex: https://search.maven.org/solrsearch/select?q=1:"[sha1sum]"&rows=20&wt=json

{
	"responseHeader": {
		"status":0,
		"QTime":6,
		"params":
			{"q":"1:\"35379fb6526fd019f331542b4e9ae2e566c57933\"",
			"core":"",
			"indent":"off",
			"fl":"id,g,a,v,p,ec,timestamp,tags",
			"start":"",
			"sort":"score desc,timestamp desc,g asc,a asc,v desc",
			"rows":"20",
			"wt":"json",
			"version":"2.2"
			}
	},
	"response": {
		"numFound":1,
		"start":0,
		"docs": [{
			"id":"org.eclipse.jetty:jetty-webapp:7.3.0.v20110203",
			"g":"org.eclipse.jetty",
			"a":"jetty-webapp",
			"v":"7.3.0.v20110203",
			"p":"jar",
			"timestamp":1296751450000,
			"ec":[
				"-sources.jar",
				"-javadoc.jar",
				"-config.jar",
				".jar",
				".pom"
			],
			"tags": [
				"application",
				"support",
				"jetty"
			]
		}]
	}
}
"""

