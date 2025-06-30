#!/bin/bash

set -e


echo "> Updating Readme"
python add_pngs_to_readme.py
echo "> Pushing to git "
git add .
git commit -m "poyo"
git push

