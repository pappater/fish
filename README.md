# fish

A simple image gallery page that displays colorful fish-themed images.

## Adding New Images

To add new images to the gallery:

1. Upload your image file to the `images/` folder (supports: jpg, jpeg, png, gif, svg, webp)
2. Commit and push your changes
3. GitHub Actions will automatically detect the new images and deploy the updated gallery

**That's it!** The image list is automatically generated during deployment - no manual editing required.

## Local Development

To test locally:
```bash
python3 -m http.server 8000
# Then open http://localhost:8000 in your browser
```

## Deployment

This site automatically deploys to GitHub Pages when changes are pushed to the `main` branch.