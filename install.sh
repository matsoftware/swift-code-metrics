#!/bin/bash

set -e

top="$(dirname "$0")"
python3 -m venv "${top}"/venv

pip_install="${top}/venv/bin/python3 ${top}/venv/bin/pip3 install"

$pip_install --upgrade "pip>=23.0"

$pip_install wheel

if arch | grep -q 'arm64'; then
    echo "Overriding pygraphviz setup for M1 architecture"
    $pip_install --global-option=build_ext --global-option="-I$(brew --prefix graphviz)/include" --global-option="-L$(brew --prefix graphviz)/lib" pygraphviz
fi

$pip_install -r requirements.txt

$pip_install -r tests-requirements.txt