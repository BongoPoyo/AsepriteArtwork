#!/bin/bash

# Exit on error
set -e

# File to modify
README="README.md"

# Backup the current README
cp "$README" "$README.bak"

# Optional: clear existing image entries (uncomment to enable)
# sed -i '/!\[.*\](.*\.png)/d' "$README"

echo -e "\n## PNG Images" >> "$README"

# Find all .png files and add them to the README
find . -type f -name "*.png" | sort | while read -r file; do
    # Remove leading ./ and escape spaces
    clean_path="${file#./}"
    echo "Adding $clean_path"
    echo "![${clean_path}](./${clean_path})" >> "$README"
done

echo "✅ PNG images added to $README"

