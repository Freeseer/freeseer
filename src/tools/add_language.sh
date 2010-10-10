#! /bin/bash
 
 if [ ! -z $1 ]; then
   echo "Creating Language prefix $1"
   ./create_language.py $1
 fi
echo "Creating profile: .."
./create_pro.py > freeseer.pro
echo "Creating .ts files: ..."
pylupdate4 freeseer.pro
rm freeseer.pro
rm languages.txt
echo "Language Files Generated"