#!/usr/bin/bash

set -e

function handle_error(){
    echo "Error occurred. Quitting installation."
    exit 1
}

function install_pytgpt(){
    if [ -z "$(which python3 -m pytgpt --help)" ]; then
       echo "Installing python-tgpt"
       pip3 install python-tgpt[cli] -U
    fi
}

function install_push(){
    echo "Adding push to path"
    chmod +x main.py
    sudo cp main.py /usr/local/bin/push
    sudo cp sanitizer.py /usr/local/bin/commit-sanitizer
}

function add_entries_to_zshrc(){
    echo "Updating zshrc"
    cat zshrc >> ~/.zshrc
}

trap handle_error ERR

install_pytgpt
install_push
add_entries_to_zshrc
echo "Push installed successfully."
push --help