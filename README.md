# Jar-Version-Finder
Ant builds do not use version numbers, Maven does. Going from Ant to Maven can be made a hassle by trying to find the versions old jars/ears/wars have used.
Uses a python script to find jars in a directory. Calculates their sha 1 checksums and searches https://repository.sonatype.org/ with it. Outputs a csv with the format

FILE NAME | GROUPID | ARTIFACTID | VERSION | DATE UPLOADED | FILETYPE | CHECKSUM
--------- | ------- | ---------- | ------- | ------------- | -------- | --------
filename1 | com.comp | thingy | 2.3 | 21-11-12 | jar | checksum1
filename2 | notFound | notFound | notFound | notFound | notfound | checksum2
filename3 | org.organ | dongy | 1.4.1 | 04-01-16 | jar | checksum3
etc  |   |   |   | | | 

in a named csv (you choose name)
