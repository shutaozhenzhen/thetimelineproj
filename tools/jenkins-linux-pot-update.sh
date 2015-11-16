#!/bin/bash

set -e

function filter_pot() {
    grep -v '^#' "$1" | grep -v 'POT-Creation-Date'
}

function fail() {
    echo "Source contains different translations"
    echo "Generate a new pot-file, commit it, and upload it to Launchpad"
    exit 1
}

cp translations/timeline.pot translations/timeline.pot.old
python tools/generate-pot-file.py
diff <(filter_pot translations/timeline.pot.old) <(filter_pot translations/timeline.pot) || fail
