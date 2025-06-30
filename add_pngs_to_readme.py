#!/usr/bin/env python3

import os
from textwrap import dedent

README = "README.md"
PNG_DIR = "png"
COLUMNS = 3  # Number of images per row in the table

# Header
header = dedent("""\
    # Aseprite Artwork
    Consists of .png and .ase of my aseprite artwork.

    ## PNG Images

    | Preview | Preview | Preview |
    |---------|---------|---------|
""")

# Collect all PNG files
png_files = []
for root, _, files in os.walk(PNG_DIR):
    for file in sorted(files):
        if file.lower().endswith(".png"):
            rel_path = os.path.join(root, file).replace("\\", "/")
            png_files.append((file, rel_path))

# Write to README.md
with open(README, "w") as readme:
    readme.write(header)

    # Create table rows
    for i in range(0, len(png_files), COLUMNS):
        row = png_files[i:i + COLUMNS]
        line = "| " + " | ".join(f"![{name}](./{path})" for name, path in row)
        line += " |" + "\n"
        readme.write(line)

print("✅ README.md rewritten with PNG preview grid.")
