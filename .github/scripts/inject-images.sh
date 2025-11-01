#!/bin/bash
set -e

# Script to automatically inject image filenames into index.html
# This scans the images/ directory and replaces the content between markers

IMAGES_DIR="images"
INDEX_FILE="index.html"

echo "Scanning ${IMAGES_DIR} directory for images..."

# Get list of image files (jpg, jpeg, png, gif, svg, webp)
# Sort them alphabetically for consistency
image_files=$(find "${IMAGES_DIR}" -maxdepth 1 -type f \( -iname "*.jpg" -o -iname "*.jpeg" -o -iname "*.png" -o -iname "*.gif" -o -iname "*.svg" -o -iname "*.webp" \) -printf "%f\n" | sort)

# Check if any images found
if [ -z "$image_files" ]; then
    echo "Warning: No image files found in ${IMAGES_DIR}/"
    image_list=""
else
    echo "Found images:"
    echo "$image_files"
    
    # Build JavaScript array entries
    image_list=""
    while IFS= read -r file; do
        if [ -z "$image_list" ]; then
            image_list="            '${file}'"
        else
            image_list="${image_list},\n            '${file}'"
        fi
    done <<< "$image_files"
fi

# Create the new content to inject
new_content="        const availableImages = [\n${image_list}\n        ];"

echo "Injecting image list into ${INDEX_FILE}..."

# Use sed to replace content between markers (BUILD_INJECT_START and BUILD_INJECT_END)
sed -i '/BUILD_INJECT_START/,/BUILD_INJECT_END/{//!d}' "${INDEX_FILE}"
sed -i "/BUILD_INJECT_START/a\\${new_content}" "${INDEX_FILE}"

echo "✓ Successfully injected image list into ${INDEX_FILE}"
