#!/usr/bin/python

import sys;
import os;

if(len(sys.argv) < 3):
  print("Usage ./create_language  language_name language_prefix");
  sys.exit(1);

LANGAUGE_DIRECTORY = '../freeseer/frontend/default/languages';  
MAIN_DIRECTORY = '../freeseer/frontend/default/';  
FORM_DIRECTORY = '../freeseer/frontend/default/forms';  

 
language_file = open(LANGAUGE_DIRECTORY+'/languages.txt' , 'a+');
languages = language_file.readlines();
languages = map(lambda x: x.rstrip().split(' '),languages);

language_names = map(lambda x: x[0],languages);
language_prefixs = map(lambda x: x[1],languages);

if(language_names.count(sys.argv[1])!=0):
  print("Error: Language Already Exists");
  sys.exit(1);
  
if(language_names.count(sys.argv[2]!=0)):
  print("Error: Language Prefix Exits");
  sys.exit(1);
    
language_file.write(sys.argv[1] + " " + sys.argv[2]+"\n");
language_file.close();








    
