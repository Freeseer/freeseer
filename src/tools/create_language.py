#!/usr/bin/python

import sys;
import os;


if(len(sys.argv) < 2):
  print("Usage ./create_language language_prefix");
  sys.exit(1);

LANGAUGE_DIRECTORY = '../freeseer/frontend/default/languages';  
MAIN_DIRECTORY = '../freeseer/frontend/default/';  
FORM_DIRECTORY = '../freeseer/frontend/default/forms';  


files = os.listdir(LANGAUGE_DIRECTORY);
files = map(lambda x: x.split('.') , files);
qm_files = filter(lambda x:x[len(x)-1] == 'qm',files);
languages_existing = map(lambda x: x[0].split("_")[1],qm_files);

language_file = open('languages.txt' , 'w');

if(languages_existing.count(sys.argv[1]!=0)):
  print("Error: Language Prefix Exits");
  sys.exit(1);
    
for languages in languages_existing:
  language_file.write(languages+"\n");
  
 
language_file.write(sys.argv[1]+"\n");
language_file.close();








    
