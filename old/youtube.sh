#!/bin/bash 
while read line  
do   
   echo "Telechargement de $line"
   youtube-dl $line  
done < file.txt
