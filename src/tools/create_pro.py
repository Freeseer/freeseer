#!/usr/bin/python

import sys;
import os;

LANGAUGE_DIRECTORY = '../freeseer/frontend/default/languages';  
MAIN_DIRECTORY = '../freeseer/frontend/default';  
FORM_DIRECTORY = '../freeseer/frontend/default/forms';  


src_files = os.listdir(MAIN_DIRECTORY);
ui_files = os.listdir(FORM_DIRECTORY);

src_files = map(lambda x:x.split('.'),src_files);
src_files = filter(lambda x: x[len(x)-1]=='py',src_files);

ui_files = map(lambda x:x.split('.'),ui_files);
ui_files = filter(lambda x: x[len(x)-1]=='ui',ui_files);

language_file = open(LANGAUGE_DIRECTORY+'/languages.txt' , 'r');
languages = language_file.readlines();
languages = map(lambda x: x.rstrip().split(' '),languages);

language_names = map(lambda x: x[0],languages);
language_prefixs = map(lambda x: x[1],languages);
language_file.close();


print('SOURCES = \\');
for i in range(0,len(src_files)):
  end = '\\';
  if(i == len(src_files)-1):
    end = '';
  print(MAIN_DIRECTORY+"/"+src_files[i][0]+'.'+src_files[i][1] + ""+ end);
  
print('FORMS = \\');
for i in range(0,len(ui_files)):
  end = '\\';
  if(i == len(ui_files)-1):
    end = '';
  print(FORM_DIRECTORY+"/"+ui_files[i][0]+'.'+ui_files[i][1] + ""+ end);

print('TRANSLATIONS = \\');
for i in range(0,len(language_prefixs)):
  end = '\\';
  if(i == len(language_prefixs)-1):
    end = '';
  print(LANGAUGE_DIRECTORY+"/"+'tr_'+language_prefixs[i] + ".ts" + end);
  
  
  
