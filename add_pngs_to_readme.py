#!/usr/bin/env python3

import os
from textwrap import dedent

README = "README.md"
PNG_DIR = "png"
COLUMNS = 3  # Number of images per row

# Header text
header = dedent("""\
    # Aseprite Artwork
    Consists of .png and .ase of my aseprite artwork.

    ## PNG Images
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

    for i in range(0, len(png_files), COLUMNS):
        row = png_files[i:i + COLUMNS]

        # Pad row with blanks if needed
        while len(row) < COLUMNS:
            row.append(("", ""))

        # Start a new table for each row
        filename_row = "| " + " | ".join(f"`{name}`" if name else " " for name, _ in row) + " |\n"
        separator_row = "| " + " | ".join("---" for _ in row) + " |\n"
        image_row = "| " + " | ".join(f"![{name}](./{path})" if name else " " for name, path in row) + " |\n"

        readme.write("\n")
        readme.write(filename_row)
        readme.write(separator_row)
        readme.write(image_row)

print("✅ README.md updated: Each image row is now a separate table.")
