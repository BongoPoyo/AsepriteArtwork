#!/bin/bash

# Exit on error
set -e

README="README.md"

# Overwrite README with the header
cat > "$README" <<EOF
# Aseprite Artwork
Consists of .png and .ase of my aseprite artwork.

## PNG Images

| Preview | Preview | Preview |
|--------|--------|--------|
EOF

count=0
row=""

# Find all .png files and sort them
find ./png -type f -name "*.png" | sort | while read -r file; do
    clean_path="${file#./}"
    filename=$(basename "$clean_path")
    image_md="![${filename}](./${clean_path})"

    # Append to current row
    row+="| $image_md "

    ((count++))
    if (( count % 3 == 0 )); then
        # Complete the row
        echo "${row}|" >> "$README"
        row=""
    fi
done

# Add any remaining images (if not divisible by 3)
if (( count % 3 != 0 )); then
    remaining=$((3 - count % 3))
    for ((i=0; i<remaining; i++)); do
        row+="| "
    done
    echo "${row}|" >> "$README"
fi

echo "✅ README.md rewritten with PNG previews in table format."

