#!/bin/bash 
mkdir video
while read line  
do   
   echo "Telechargement de $line"
   youtube-dl --ignore-config -o './video/%(title)s.%(ext)s' $line  
done < file.txt
