# first load Fiji conifg
# If Fiji.app isnt there
curl -O https://downloads.imagej.net/fiji/latest/fiji-nojre.zip
unzip fiji-nojre.zip
# If SciView is not installed
./Fiji.app/ImageJ-linux64 --update add-update-site sciview https://sites.imagej.net/SciView/
./Fiji.app/ImageJ-linux64 --update update
