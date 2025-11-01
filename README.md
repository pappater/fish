# fish

A simple image gallery page that displays colorful fish-themed images.

## Adding New Images

To add new images to the gallery:

1. Add your image file to the `images/` folder
2. Edit `index.html` and add the filename to the `availableImages` array (around line 151)
3. Commit and push your changes - the page will automatically deploy via GitHub Actions

## Local Development

To test locally:
```bash
python3 -m http.server 8000
# Then open http://localhost:8000 in your browser
```

## Deployment

This site automatically deploys to GitHub Pages when changes are pushed to the `main` branch.