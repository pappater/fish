# Art Generation Scripts

This directory contains scripts for generating AI art using Gemini API.

## generate_art.py

Automated art generation script that:

1. **Selects a random art style** from the list in `art_styles.json`
2. **Generates a detailed art concept** using Gemini AI (150-250 words with rich visual details)
3. **Saves the prompt to a public gist** (specified by `FISH_GIST_ID`)
4. **Generates an image** using Gemini's Imagen API with the art concept prompt
5. **Saves the image** to the `images/` directory
6. **Creates metadata** file with generation details

### Requirements

```bash
pip install -r requirements.txt
```

### Environment Variables

Required environment variables:

- `GEMINI_API_KEY` - Your Google Gemini API key
- `GIST_TOKEN` - GitHub personal access token with gist permissions
- `FISH_GIST_ID` - The ID of the public gist to store prompts

Optional:
- `GEMINI_MODEL` - Gemini model to use (default: `gemini-2.0-flash-exp`)

### Usage

#### Manual Execution

```bash
export GEMINI_API_KEY="your-api-key"
export GIST_TOKEN="your-gist-token"
export FISH_GIST_ID="your-gist-id"

python scripts/generate_art.py
```

#### Automated Execution

The script runs automatically via GitHub Actions:
- Daily at 6 AM UTC (configured in `.github/workflows/generate-art.yml`)
- Can be manually triggered from the Actions tab

### Output

The script creates:

1. **Image file** in `images/` directory
   - Format: `{timestamp}.png`
   - Generated using Gemini Imagen API

2. **Metadata file** in `images/` directory
   - Format: `{timestamp}_metadata.json`
   - Contains: art style, concept, gist URL, generation timestamp

3. **Gist entry** with the art concept prompt
   - Format: `art_prompt_{timestamp}.md`
   - Contains: full art concept description

### Art Styles

The script selects from 230+ art styles defined in `art_styles.json`, including:
- Historical styles (Baroque, Renaissance, Impressionism, etc.)
- Modern movements (Cubism, Surrealism, Pop Art, etc.)
- Contemporary styles (Digital art, Glitch art, AI art, etc.)
- Regional traditions (Ukiyo-e, Bengal School, Hudson River School, etc.)

Each art style gets a unique, detailed prompt that captures its distinctive characteristics, techniques, and aesthetic qualities.
