#!/bin/bash

set -e

top="$(dirname $0)"

"${top}"/venv/bin/pytest --cov=swift_code_metrics