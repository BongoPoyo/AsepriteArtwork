#!/bin/bash

set -e


echo "> python add_pngs_to_readme.py \n"
python add_pngs_to_readme.py
echo "> Pushing to git \n"
git add .
git commit -m "poyo"
git push

