#!/bin/bash

set -e

pushd tests

rm -rf report
mkdir report
python3 -m unittest

popd