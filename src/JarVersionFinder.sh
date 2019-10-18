#!/bin/bash

# find current directory #

# opens a temporary csv file # 
touch tempcsv.csv

# find all jar files in current directory #
JARFILES=./*.jar

# loop through jarfiles and save their names and checksums with sha 1 to a temporary csv file #
for jarfile in $JARFILES
do
	echo $(shasum -a 1 "$jarfile") >> tempcsv.csv
done

# jars and checksums should be listed as

#jarname1, checksum1
#jarname2, checksum2
#jarname3, checksum3
#etc...

# closes temporary csv file



# calls a python script with temporary csv file name as arguement
# PYTHON -----------------------------------------------------------------------------------------------------------------------------------
# python script takes in the checksums and compares checksum with https://repository.sonatype.org/
# python script reads csv file into pandas dataframe
# if there is a hit the groupId, artifactId, version, and age are inserted into a pandas dataframe
# Python saves pandas dataframe to a new output csv file that you can name

# data looks like
# JAR NAME, 	GROUPID, 	ARTIFACTID, 	VERSION, 	DATE UPLOADED, 	CHECKSUM
# jarname1, 	com.comp, 	thingy, 	2.3, 		21-11-12, 	checksum1
# jarname2, 	notFound, 	notFound, 	notFound, 	notFound,	checksum2
# jarname3, 	org.organ,	dongy,		1.4.1,		04-01-16,	checksum3 
# etc


# BASH -------------------------------------------------------------------------------------------------------------------------------------

# deletes temporary csv file

