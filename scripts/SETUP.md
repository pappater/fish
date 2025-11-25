# Setup Instructions for Art Generation

## Prerequisites

### 1. Google Gemini API Access

You need access to Google's Gemini API for text generation (art concept prompts):

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create or select a project
3. Generate an API key
4. Ensure your API key has access to Gemini models for text generation

### 2. Image Generation Provider

Choose one of the supported image generation providers:

#### Option A: OpenAI DALL-E (Recommended)

OpenAI's DALL-E is recommended for more reliable image generation with better quota limits.

1. Go to [OpenAI Platform](https://platform.openai.com/api-keys)
2. Create an account and add billing information
3. Generate an API key
4. Set `IMAGE_PROVIDER=openai` in your environment

**Available Models:**
- `dall-e-3` (default) - Highest quality, supports 1024x1024, 1024x1792, 1792x1024
- `dall-e-2` - Faster, supports 256x256, 512x512, 1024x1024

#### Option B: Google Gemini/Imagen

Use Gemini's built-in image generation (may have rate limits on free tier).

1. Ensure your Gemini API key has image generation permissions
2. Set `IMAGE_PROVIDER=gemini` in your environment (default)

**Note**: Gemini's free tier has strict rate limits. If you encounter quota errors, consider:
- Switching to OpenAI DALL-E
- Using Vertex AI Imagen (requires GCP billing)
- Upgrading to a paid Gemini plan

### 3. GitHub Gist Setup

1. Create a GitHub personal access token:
   - Go to GitHub Settings → Developer settings → Personal access tokens → Tokens (classic)
   - Click "Generate new token (classic)"
   - Select scopes: `gist` (create and edit gists)
   - Save the token securely

2. Create a public gist:
   - Go to https://gist.github.com/
   - Create a new public gist (any content, will be updated by script)
   - Note the Gist ID from the URL: `https://gist.github.com/username/{GIST_ID}`

### 4. GitHub Repository Secrets

Add these secrets to your GitHub repository:

1. Go to your repository → Settings → Secrets and variables → Actions
2. Add the following secrets:

**Required Secrets:**
- `GEMINI_API_KEY`: Your Google Gemini API key (for text generation)
- `GIST_TOKEN`: Your GitHub personal access token
- `FISH_GIST_ID`: The ID of your public gist

**Image Provider Secrets (choose one):**

For OpenAI DALL-E:
- `IMAGE_PROVIDER`: Set to `openai`
- `OPENAI_API_KEY`: Your OpenAI API key
- `OPENAI_IMAGE_MODEL`: (Optional) `dall-e-3` (default) or `dall-e-2`
- `OPENAI_IMAGE_SIZE`: (Optional) `1024x1024` (default), `1024x1792`, or `1792x1024`
- `OPENAI_IMAGE_QUALITY`: (Optional) `standard` (default) or `hd` (DALL-E 3 only)

For Gemini/Imagen:
- `IMAGE_PROVIDER`: Set to `gemini` (or leave unset, it's the default)
- `GEMINI_IMAGE_MODEL`: (Optional) Gemini image model name

**Optional Secrets:**
- `GEMINI_MODEL`: Gemini model for text generation (default: `gemini-2.0-flash-exp`)
- `SKIP_IMAGE_GENERATION`: Set to `true` to skip image generation

## Local Development

### Installation

```bash
# Install Python dependencies
pip install -r requirements.txt
```

### Environment Variables

Create a `.env` file or export these variables:

```bash
# Required
export GEMINI_API_KEY="your-gemini-api-key"
export GIST_TOKEN="your-github-token"
export FISH_GIST_ID="your-gist-id"

# Image provider (choose one)
export IMAGE_PROVIDER="openai"  # or "gemini"

# For OpenAI DALL-E
export OPENAI_API_KEY="your-openai-api-key"
export OPENAI_IMAGE_MODEL="dall-e-3"  # optional
export OPENAI_IMAGE_SIZE="1024x1024"  # optional
export OPENAI_IMAGE_QUALITY="standard"  # optional

# For Gemini/Imagen
export GEMINI_IMAGE_MODEL="gemini-2.5-flash-preview-05-20"  # optional

# Text generation (optional)
export GEMINI_MODEL="gemini-2.0-flash-exp"
```

### Running Locally

```bash
python scripts/generate_art.py
```

## Provider Comparison

| Feature | OpenAI DALL-E | Gemini/Imagen |
|---------|---------------|---------------|
| Rate Limits | Higher quotas | Strict free tier limits |
| Image Quality | Excellent | Good |
| Price | Pay per image | Free tier available |
| Setup | Requires billing | May require GCP for production |
| Recommended For | Production use | Testing/experimentation |

## Troubleshooting

### Rate Limit / Quota Exceeded Errors

If you see "429 You exceeded your current quota" errors:

1. **Switch to OpenAI**: Set `IMAGE_PROVIDER=openai` and configure `OPENAI_API_KEY`
2. **Wait and retry**: Gemini free tier limits reset periodically
3. **Upgrade plan**: Consider a paid Gemini or Vertex AI plan
4. **Skip images**: Set `SKIP_IMAGE_GENERATION=true` to only generate prompts

### "Model not found" Error

- Verify your API key has access to the specified model
- Check if the model name is correct
- For Gemini, ensure you have image generation permissions

### OpenAI Authentication Errors

- Verify your `OPENAI_API_KEY` is correct
- Ensure your OpenAI account has billing enabled
- Check that you have API access (not just ChatGPT Plus)

### Gist Update Failures

- Verify your `GIST_TOKEN` has `gist` scope
- Check that `FISH_GIST_ID` is correct
- Ensure the gist is public

## Support

For issues related to:
- **Gemini API**: Check [Google AI Studio documentation](https://ai.google.dev/)
- **OpenAI API**: Check [OpenAI API documentation](https://platform.openai.com/docs)
- **Script issues**: Open an issue in this repository
