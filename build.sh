# Tuottaa riippumattoman binäärin
# oletuksena pyinstaller asennettuna
# pyinstallerin asennus lokaaliin:
# pip3 install pyinstaller

if [ -d "dist/" ]; then rm -R dist/; fi
if [ -d "build/" ]; then rm -R build/; fi

pyinstaller src/__main__.py -F
mv dist/__main__ dist/ohtu-miniprojekti
cp -R storage/ dist/
cp iceberg.db dist/storage/app.db

# hakee viimeisimmän käytetyn tagin versionumeroksi
VERSION=`git describe --tags --abbrev=0`

mv dist ohtu-miniprojekti
if ! [ -d "releases/" ]; then mkdir releases; fi
if [ -f "./ohtu-miniprojekti-temp.tar.gz" ]; then rm ./ohtu-miniprojekti-temp.tar.gz; fi
# cd dist/ && tar -zcvf ../ohtu-miniprojekti-temp.tar . && cd - 
tar -czvf ohtu-miniprojekti-temp.tar.gz ohtu-miniprojekti
mv ohtu-miniprojekti-temp.tar.gz releases/ohtu-miniprojekti-$VERSION.tar.gz

rm -R ohtu-miniprojekti/
rm -R build/