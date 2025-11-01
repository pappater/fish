#!/bin/bash
set -e

# Script to automatically inject image filenames into index.html
# This scans the images/ directory and replaces the content between markers

IMAGES_DIR="images"
INDEX_FILE="index.html"
TEMP_FILE="${INDEX_FILE}.tmp"

echo "Scanning ${IMAGES_DIR} directory for images..."

# Get list of image files (jpg, jpeg, png, gif, svg, webp) - portable version
# Works with both GNU find and BSD find
image_files=$(find "${IMAGES_DIR}" -maxdepth 1 -type f \( -iname "*.jpg" -o -iname "*.jpeg" -o -iname "*.png" -o -iname "*.gif" -o -iname "*.svg" -o -iname "*.webp" \) -exec basename {} \; | sort)

# Check if any images found
if [ -z "$image_files" ]; then
    echo "Warning: No image files found in ${IMAGES_DIR}/"
    image_list=""
else
    echo "Found images:"
    echo "$image_files"
    
    # Build JavaScript array entries with proper newlines
    image_list=""
    while IFS= read -r file; do
        if [ -z "$image_list" ]; then
            image_list="            '${file}'"
        else
            image_list="${image_list},"$'\n'"            '${file}'"
        fi
    done <<< "$image_files"
fi

echo "Injecting image list into ${INDEX_FILE}..."

# Use awk for portable, cross-platform text replacement
awk -v img_list="$image_list" '
    /BUILD_INJECT_START/ {
        print
        print "        const availableImages = ["
        if (img_list != "") {
            print img_list
        }
        print "        ];"
        skip = 1
        next
    }
    /BUILD_INJECT_END/ {
        skip = 0
    }
    !skip
' "${INDEX_FILE}" > "${TEMP_FILE}"

# Replace original file with updated version
mv "${TEMP_FILE}" "${INDEX_FILE}"

echo "✓ Successfully injected image list into ${INDEX_FILE}"
