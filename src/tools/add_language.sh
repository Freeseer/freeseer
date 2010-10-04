#! /bin/bash
cd ..
echo "Cleaning the Build:..."
make clean > hide_output
cd tools;

 
 if [ ! -z $1 ]; then
   echo "Creating Language $1 with prefix $2"
   ./create_language.py $1 $2
 fi
echo "Creating profile: .."
./create_pro.py > freeseer.pro
echo "Creating .ts files: ..."
pylupdate4 freeseer.pro
rm freeseer.pro
cd ..
echo "Rebuilding: ... "
make > hide_output
rm hide_output