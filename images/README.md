# Images Folder

Place your images in this folder to display them in the gallery.

## How to add images:

1. **Quick method** (auto-detection):
   - Simply add images to this folder with common naming patterns like:
     - `1.jpg`, `2.jpg`, `3.png`, etc.
     - `image1.jpg`, `image2.png`, etc.
   - The gallery will automatically try to load them

2. **Manual method** (recommended for production):
   - Edit the `index.html` file
   - Find the commented section with the `images` array
   - Uncomment it and add your image filenames
   - This ensures only your images are loaded

## Supported formats:
- JPG/JPEG
- PNG
- GIF
- WebP

The gallery uses lazy loading for optimal performance!
