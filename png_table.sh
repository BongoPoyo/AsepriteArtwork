#!/bin/bash

# Exit on error and show commands
set -eo pipefail

README="README.md"
PNG_DIR="./png"

# Create directory if it doesn't exist
mkdir -p "$PNG_DIR"

# Overwrite README with the header
cat > "$README" <<EOF
# Aseprite Artwork
Consists of .png and .ase of my aseprite artwork.

## PNG Images

<div class="grid">
EOF

# Find and process PNG files safely
while IFS= read -r -d '' file; do
    filename=$(basename "$file")
    # Properly escape special characters in paths
    file_path=$(printf "%q" "$file" | sed "s/'//g")
    echo -e "<div class=\"grid-item\">\n"***${filename}***"\n<img src=\"${file_path}\" alt=\"${filename}\" width=\"200\">\n</div>"
done < <(find "$PNG_DIR" -type f -name "*.png" -print0 | sort -z) >> "$README"

# Close the grid and add CSS
cat >> "$README" <<EOF
</div>

<style>
.grid {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
  padding: 16px;
}
.grid-item {
  flex: 1 1 auto;
  height: 200px;
  overflow: hidden;
}
.grid-item img {
  width: 100%;
  height: 100%;
  object-fit: contain;
}
</style>
EOF

echo "✅ README.md updated with PNG grid"
