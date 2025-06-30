#!/bin/bash

# Exit on error
set -e

README="README.md"

# Overwrite README with the header
cat > "$README" <<EOF
# Aseprite Artwork
Consists of .png and .ase of my aseprite artwork.

## PNG Images

<div class="grid" markdown="1">
EOF

# Find all .png files and arrange in a grid
find ./png -type f -name "*.png" | sort | while read -r file; do
    clean_path="${file#./}"
    filename=$(basename "$clean_path")
    echo -e "<div class=\"grid-item\" markdown=\"1\">\n![${filename}](./${clean_path})\n</div>" >> "$README"
done

# Close the grid div
echo -e "\n</div>\n<style>\n.grid {\n  display: flex;\n  flex-wrap: wrap;\n  gap: 10px;\n}\n.grid-item {\n  flex: 1 1 200px;\n  max-width: 300px;\n}\n</style>" >> "$README"

echo "✅ README.md rewritten with PNG previews in grid format."
