#!/bin/bash

# Exit on error
set -e

README="README.md"

# Overwrite README with the header
cat > "$README" <<EOF
# Aseprite Artwork
Consists of .png and .ase of my aseprite artwork.

## PNG Images
EOF


# Find all .png files and append filename + preview
find ./png -type f -name "*.png" | sort | while read -r file; do
    clean_path="${file#./}"
    filename=$(basename "$clean_path")
    
    echo -e "\n### ${filename}" >> "$README"
    echo "![${filename}](./${clean_path})" >> "$README"
done

echo "✅ README.md rewritten with PNG previews."

