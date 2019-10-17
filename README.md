# Jar-Version-Finder
Ant builds do not use version numbers, Maven does. Going from Ant to Maven can be made a hassle by trying to find the versions old jars have used.
Uses a bash script to find jars and their checksums and compares them to https://repository.sonatype.org/ with a python script, saves data like 

JAR NAME | GROUPID | ARTIFACTID | VERSION | DATE UPLOADED | CHECKSUM
---------- | ------- | ---------- | ------- | ------------- | ----------
jarname1 | com.comp | thingy | 2.3 | 21-11-12 | checksum1
jarname2 | notFound | notFound | notFound | notFound | checksum2
jarname3 | org.organ | dongy | 1.4.1 | 04-01-16 | checksum3
etc  |   |   |   |    | 

in a named csv (you choose name)
