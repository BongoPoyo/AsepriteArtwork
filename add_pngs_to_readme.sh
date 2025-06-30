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

# Begin the table
echo -e "\n| Preview | Preview | Preview |" >> "$README"
echo "|---|---|---|" >> "$README"

count=0
row=""

# Find all .png files and arrange in a 3-column table
find ./png -type f -name "*.png" | sort | while read -r file; do
    clean_path="${file#./}"
    filename=$(basename "$clean_path")
    image_md="![${filename}](./${clean_path})"

    row+="| $image_md "

    ((count++))
    if (( count % 3 == 0 )); then
        echo "${row}|" >> "$README"
        row=""
    fi
done

# Print remaining images in the last row if not complete
if (( count % 3 != 0 )); then
    # Fill the remaining columns with empty cells
    for ((i = count % 3; i < 3; i++)); do
        row+="| "
    done
    echo "${row}|" >> "$README"
fi

echo "✅ README.md rewritten with PNG previews in table format."


