#!/bin/bash

set -e

top="$(dirname "$0")"
python3 -m venv "${top}"/venv

"${top}"/venv/bin/python3 ${top}/venv/bin/pip install --upgrade "pip>=23.0"

"${top}"/venv/bin/python3 "${top}"/venv/bin/pip3 install wheel

if arch | grep -q 'arm64'; then
    echo "Overriding pygraphviz setup for M1 architecture"
    "${top}"/venv/bin/python3 "${top}"/venv/bin/pip3 install --global-option=build_ext --global-option="-I$(brew --prefix graphviz)/include" --global-option="-L$(brew --prefix graphviz)/lib" pygraphviz
fi

"${top}"/venv/bin/python3 "${top}"/venv/bin/pip3 install -r requirements.txt

"${top}"/venv/bin/python3 "${top}"/venv/bin/pip3 install -r tests-requirements.txt