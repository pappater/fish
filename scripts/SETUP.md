# Setup Instructions for Art Generation

## Prerequisites

### 1. Google Gemini API Access

You need access to Google's Gemini API with image generation capabilities:

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create or select a project
3. Generate an API key
4. Ensure your API key has access to:
   - Gemini models for text generation (gemini-2.0-flash-exp or similar)
   - Imagen models for image generation (imagen-3.0-generate-001)

**Note**: Image generation with Gemini/Imagen may require:
- Specific API access (not all API keys have image generation enabled)
- Vertex AI access for production use
- Google Cloud Platform project with billing enabled

### 2. GitHub Gist Setup

1. Create a GitHub personal access token:
   - Go to GitHub Settings → Developer settings → Personal access tokens → Tokens (classic)
   - Click "Generate new token (classic)"
   - Select scopes: `gist` (create and edit gists)
   - Save the token securely

2. Create a public gist:
   - Go to https://gist.github.com/
   - Create a new public gist (any content, will be updated by script)
   - Note the Gist ID from the URL: `https://gist.github.com/username/{GIST_ID}`

### 3. GitHub Repository Secrets

Add these secrets to your GitHub repository:

1. Go to your repository → Settings → Secrets and variables → Actions
2. Add the following secrets:

   - `GEMINI_API_KEY`: Your Google Gemini API key
   - `GIST_TOKEN`: Your GitHub personal access token
   - `FISH_GIST_ID`: The ID of your public gist
   - `GEMINI_MODEL`: (Optional) Gemini model name (default: gemini-2.0-flash-exp)

## Local Development

### Installation

```bash
# Install Python dependencies
pip install -r requirements.txt
```

### Environment Variables

Create a `.env` file or export these variables:

```bash
export GEMINI_API_KEY="your-gemini-api-key"
export GIST_TOKEN="your-github-token"
export FISH_GIST_ID="your-gist-id"
export GEMINI_MODEL="gemini-2.0-flash-exp"  # optional
```

### Running Locally

```bash
python scripts/generate_art.py
```

## API Availability Notes

### Image Generation Status

As of the latest update, Google's Gemini API for image generation (Imagen) has the following requirements:

1. **Imagen API Access**: 
   - Available through Vertex AI
   - Requires Google Cloud Project with billing
   - Not all Gemini API keys include image generation

2. **Alternative Solutions**:
   - Use Vertex AI Imagen API (requires GCP setup)
   - Use other image generation services (DALL-E, Stable Diffusion, etc.)
   - Integrate with external APIs that support text-to-image

3. **Current Implementation**:
   - Script generates detailed art concept prompts (always works)
   - Saves prompts to GitHub Gist (always works)
   - Image generation requires Imagen API access (may need updates)

### Updating for Image Generation

If you have Imagen API access through Vertex AI, you may need to:

1. Install additional dependencies:
   ```bash
   pip install google-cloud-aiplatform
   ```

2. Use Vertex AI credentials:
   ```bash
   export GOOGLE_APPLICATION_CREDENTIALS="/path/to/credentials.json"
   export GCP_PROJECT_ID="your-project-id"
   export GCP_LOCATION="us-central1"
   ```

3. Update the image generation function to use Vertex AI Imagen API

## Troubleshooting

### "Model not found" Error

If you get errors about the Imagen model not being available:
- Verify your API key has image generation access
- Check if you need to use Vertex AI instead
- Consider using alternative image generation APIs

### Gist Update Failures

If gist updates fail:
- Verify your GIST_TOKEN has `gist` scope
- Check that FISH_GIST_ID is correct
- Ensure the gist is public

### Rate Limits

Google APIs have rate limits:
- Gemini API: Typically 60 requests per minute
- Imagen API: May have lower limits
- Adjust the GitHub Actions schedule if you hit rate limits

## Support

For issues related to:
- **Gemini API**: Check [Google AI Studio documentation](https://ai.google.dev/)
- **Imagen API**: Check [Vertex AI Imagen documentation](https://cloud.google.com/vertex-ai/docs/generative-ai/image/overview)
- **Script issues**: Open an issue in this repository
