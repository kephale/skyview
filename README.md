#

1) `conda env create -f skyview.yml`
2) run `setup.sh`  
3) clone the sciview repository
4) in the sciview repository (assumes skyview and sciview are in same parent directory):
```
git checkout janelia-minihackathon
mvn package
cp target/sciview-0.2.0-beta-2-SNAPSHOT.jar ../skyview/Fiji.app/jars/
```
