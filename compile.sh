[ -d bin ] || mkdir bin
bin="$(realpath bin)" && cd bin
loc="/home/$USER/.local"
python="$(which python3)"

$python -m pip install -r ../requirements.txt
pyinstaller --clean --onefile ../clyp.py
pyinstaller --clean --onefile ../prep.py
[ -d ../temp ] || mkdir ../temp
mv ./dist/* ../temp && rm -rf ./* && mv ../temp/* . && rm -rf ../temp

[ -d $loc ] || mkdir -p $loc/bin
cp -r ./* $loc/bin
echo -e "\n\e[32mCompiled to $loc/bin and left copies in $bin\e[0m"