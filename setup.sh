# first load Fiji conifg
# If Fiji.app isnt there
if ! unzip -tqq fiji-nojre.zip; then
  echo
  echo "--> Downloading Fiji"
  curl -L -O https://downloads.imagej.net/fiji/latest/fiji-nojre.zip ||
    die "Could not download Fiji"
fi

if [ ! -f fiji-nojre.zip ]
then
  echo "--> Unpacking Fiji"
  rm -rf Fiji.app
  unzip fiji-nojre.zip || die "Could not unpack Fiji"
fi

# If SciView is not installed
if [[ "$OSTYPE" == "linux-gnu" ]]; then
  BINARY=ImageJ-linux64
elif [[ "$OSTYPE" == "darwin"* ]]; then
  BINARY=Contents/MacOS/ImageJ-macosx
elif [[ "$OSTYPE" == "cygwin" ]]; then
  BINARY=ImageJ-win64.exe
elif [[ "$OSTYPE" == "msys" ]]; then
  BINARY=ImageJ-win64.exe
elif [[ "$OSTYPE" == "win32" ]]; then
  BINARY=ImageJ-win32.exe
else
  echo "Sorry, but your operating system is not supported by Fiji."
  exit 1
fi

echo "--> Adding SciView-Unstable update site"
./Fiji.app/$BINARY --update add-update-site SciView-Unstable https://sites.imagej.net/SciView-Unstable/
echo "--> Updating Fiji"
./Fiji.app/$BINARY --update update
echo "--> Done."
