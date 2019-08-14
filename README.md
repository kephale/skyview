#

1) run `setup.sh`  
2) clone the sciview repository
3) in the sciview repository (assumes scyview and sciview are in same parent directory):
```
git checkout janelia-minihackathon
mvn package
cp target/sciview-0.2.0-beta-2-SNAPSHOT.jar ../scyview/Fiji.app/jars/
```
