trap terminate INT
function terminate() {
    # Trapped so echo does not work on line 42 when incomplete.
    echo -e "\e[31mNot compeleted\e[0m" && exit 1
}

# Create bin/ to put copies of the compiled files if it does not exist.
[ -d bin ] || mkdir bin

bin="$(realpath bin)" && cd bin
loc="/home/$USER/.local"
python="$(which python3)" # Assumming Python3 is installed.

# Verify Python version 3 and above is installed and use that.
if [ -z $python ]; then
    if [ -n "$(which python)" ]; then
        [[ -z "$(python -V | grep -P ' [3-9]')" ]] &&
            echo "Python version 3 and above is required, install, or add it to path then try again." && exit 1
    else
        echo "Please install Python3 or add it to path then try again." && exit 1
    fi

    python=python
fi

# Install requirements from requirements.txt.
$python -m pip install -r ../requirements.txt

# Loop through scripts/ for Python scripts to then compile.
for script in ../scripts/*.py; do
    pyinstaller --clean --onefile "$(realpath $script)"
done

[ -d ../temp ] || mkdir ../temp

# I'm not explaining this.
mv dist/* ../temp && rm -rf ./* && mv ../temp/* . && rm -rf ../temp

# Create /home/$USER/.local/bin if it does not exists.
[ -d $loc ] || mkdir -p $loc/bin

cp ./* $loc/bin && echo -e "\n\e[32mCompiled to $loc/bin and left copies in $bin\e[0m"

# Check if /home/$USER/.local/bin is in path, if not, give a warning to add it.
[ -z "$(echo $PATH | grep -P :?$loc/bin/?)" ] &&
    echo -e "$loc/bin not in path, you might want to add it: \e[36mexport\e[0m PATH=\e[33m\"$(realpath $loc/bin):\e[0;35m\$PATH\e[33m\"\e[0m\n"