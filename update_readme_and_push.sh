#!/bin/bash

set -e

python add_pngs_to_readme.py
git add .
git commit -m "poyo"
git push

