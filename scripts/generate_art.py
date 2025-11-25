#!/usr/bin/env python3
"""
Art Style Image Generator
Picks an art style, generates a detailed art concept using Gemini,
saves the prompt to a public gist, then generates an image using Gemini.

Note: Image generation requires access to Gemini's Imagen API. If not available,
the script will still generate and save the art concept prompt to the gist.
"""

import os
import sys
import json
import random
import time
from datetime import datetime, timezone
from pathlib import Path
import base64

import google.generativeai as genai
from github import Github, Auth, InputFileContent


# Custom exception for image generation failures
class ImageGenerationError(Exception):
    """Raised when image generation fails but should not stop the entire process."""
    pass

# Configuration
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
GEMINI_MODEL = os.environ.get("GEMINI_MODEL", "gemini-2.0-flash-exp")
GEMINI_IMAGE_MODEL = os.environ.get("GEMINI_IMAGE_MODEL", "gemini-2.5-flash-preview-05-20")
GIST_TOKEN = os.environ.get("GIST_TOKEN")
FISH_GIST_ID = os.environ.get("FISH_GIST_ID")
SKIP_IMAGE_GENERATION = os.environ.get("SKIP_IMAGE_GENERATION", "false").lower() == "true"

# Retry configuration for API calls
MAX_RETRIES = int(os.environ.get("MAX_RETRIES", "3"))
INITIAL_RETRY_DELAY = float(os.environ.get("INITIAL_RETRY_DELAY", "20.0"))

# Paths
SCRIPT_DIR = Path(__file__).parent
REPO_ROOT = SCRIPT_DIR.parent
IMAGES_DIR = REPO_ROOT / "images"
ART_STYLES_FILE = REPO_ROOT / "art_styles.json"


def load_json(filepath):
    """Load JSON content from a file."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"ERROR: File not found: {filepath}")
        sys.exit(1)


def select_random_art_style():
    """Select a random art style from the art_styles.json file."""
    art_data = load_json(ART_STYLES_FILE)
    if not art_data or "art_styles" not in art_data:
        print("ERROR: Could not load art styles from art_styles.json")
        sys.exit(1)
    
    art_styles = art_data["art_styles"]
    if not art_styles:
        print("ERROR: Art styles list is empty")
        sys.exit(1)
    
    selected = random.choice(art_styles)
    print(f"Selected art style: {selected}")
    return selected


def generate_art_concept(art_style):
    """
    Generate a detailed art concept prompt using Gemini AI.
    
    Args:
        art_style: The art style to generate a concept for
    
    Returns:
        str: Detailed art concept prompt
    """
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel(GEMINI_MODEL)
        
        prompt = f"""You are an expert art director and creative visionary. Generate a highly detailed and evocative art concept prompt in the style of "{art_style}".

Your prompt should be rich with:
- Visual details (colors, textures, composition, lighting)
- Mood and atmosphere
- Specific artistic techniques characteristic of {art_style}
- Subject matter that exemplifies this style
- Technical specifications (perspective, proportions, medium details)

The prompt should be 150-250 words and be specific enough that an AI image generator can create a high-quality, authentic representation of {art_style}.

Format your response as a single, flowing paragraph without any headers or meta-commentary. Begin directly with the art concept description."""

        print(f"Generating art concept for {art_style}...")
        response = model.generate_content(prompt)
        
        return response.text.strip()
    except Exception as e:
        print(f"ERROR: Failed to generate art concept: {e}")
        sys.exit(1)


def save_prompt_to_gist(art_style, art_concept):
    """
    Save the art concept prompt to a public GitHub Gist.
    
    Args:
        art_style: The art style name
        art_concept: The detailed art concept prompt
    
    Returns:
        str: URL to the gist
    """
    try:
        # Validate credentials
        if not GIST_TOKEN:
            print("ERROR: GIST_TOKEN environment variable is not set")
            sys.exit(1)
        if not FISH_GIST_ID:
            print("ERROR: FISH_GIST_ID environment variable is not set")
            sys.exit(1)
        
        # Connect to GitHub
        g = Github(auth=Auth.Token(GIST_TOKEN))
        user = g.get_user()
        
        # Get or create gist
        try:
            gist = g.get_gist(FISH_GIST_ID)
            print(f"Found existing gist: {FISH_GIST_ID}")
        except Exception as e:
            print(f"ERROR: Could not access gist {FISH_GIST_ID}: {e}")
            sys.exit(1)
        
        # Create filename with timestamp (UTC)
        now_utc = datetime.now(timezone.utc)
        timestamp = now_utc.strftime("%Y%m%d_%H%M%S")
        filename = f"art_prompt_{timestamp}.md"
        
        # Create markdown content
        content = f"""# Art Concept: {art_style}

**Generated:** {now_utc.strftime("%Y-%m-%d %H:%M:%S UTC")}

**Art Style:** {art_style}

## Art Concept Prompt

{art_concept}

---

*This prompt was generated using Gemini AI and is used to create AI-generated artwork.*
"""
        
        # Update gist
        print(f"Saving prompt to gist as {filename}...")
        files = {filename: InputFileContent(content)}
        gist.edit(files=files)
        
        gist_url = f"https://gist.github.com/{user.login}/{FISH_GIST_ID}#{filename}"
        print(f"✓ Prompt saved to gist: {gist_url}")
        
        return gist_url
    except Exception as e:
        print(f"ERROR: Failed to save prompt to gist: {e}")
        sys.exit(1)


def generate_image(art_concept, art_style):
    """
    Generate an image using Gemini's Imagen API based on the art concept prompt.
    
    Note: This uses the Imagen API through Gemini's generative model.
    The model is configured via GEMINI_IMAGE_MODEL environment variable.
    Includes retry logic with exponential backoff for rate limit errors.
    
    Args:
        art_concept: The detailed art concept prompt
        art_style: The art style name (for filename)
    
    Returns:
        str: Path to the saved image file
    """
    genai.configure(api_key=GEMINI_API_KEY)
    
    # Use Imagen model for image generation
    print(f"Generating image for {art_style}...")
    print(f"Using prompt: {art_concept[:100]}...")
    print(f"Using image model: {GEMINI_IMAGE_MODEL}")
    
    # Use the image model from environment variable
    imagen_model = genai.GenerativeModel(GEMINI_IMAGE_MODEL)
    
    last_exception = None
    
    for attempt in range(MAX_RETRIES):
        try:
            # Generate image with the art concept prompt
            response = imagen_model.generate_content(art_concept)
            
            # Save image (using UTC timestamp)
            timestamp = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
            image_filename = f"{timestamp}.png"
            image_path = IMAGES_DIR / image_filename
            
            # Ensure images directory exists
            IMAGES_DIR.mkdir(parents=True, exist_ok=True)
            
            # Extract image data from response
            # The response should contain image data in parts
            if response and hasattr(response, 'parts'):
                for part in response.parts:
                    if hasattr(part, 'inline_data'):
                        # Validate image data before writing
                        image_data = part.inline_data.data
                        if image_data and len(image_data) > 0:
                            with open(image_path, "wb") as f:
                                f.write(image_data)
                            print(f"✓ Image saved to {image_path}")
                            return str(image_path)
                        else:
                            print("WARNING: Image data is empty or None")
            
            # If we reach here, try alternative format
            if hasattr(response, '_result'):
                result = response._result
                if hasattr(result, 'candidates') and result.candidates:
                    candidate = result.candidates[0]
                    if hasattr(candidate, 'content') and hasattr(candidate.content, 'parts'):
                        for part in candidate.content.parts:
                            if hasattr(part, 'inline_data'):
                                # Validate image data before writing
                                image_data = part.inline_data.data
                                if image_data and len(image_data) > 0:
                                    with open(image_path, "wb") as f:
                                        f.write(image_data)
                                    print(f"✓ Image saved to {image_path}")
                                    return str(image_path)
                                else:
                                    print("WARNING: Image data is empty or None")
            
            print("ERROR: Could not extract image data from response")
            raise ImageGenerationError("No valid image data found in response")
            
        except Exception as e:
            last_exception = e
            error_str = str(e)
            error_type = type(e).__name__
            
            # Check if this is a rate limit error (429) that can be retried
            is_rate_limit = "429" in error_str or "ResourceExhausted" in error_type or "quota" in error_str.lower()
            
            if is_rate_limit and attempt < MAX_RETRIES - 1:
                # Calculate delay with exponential backoff
                delay = INITIAL_RETRY_DELAY * (2 ** attempt)
                print(f"Rate limit hit (attempt {attempt + 1}/{MAX_RETRIES}). Retrying in {delay:.1f} seconds...")
                time.sleep(delay)
                continue
            else:
                # Either not a rate limit error or we've exhausted retries
                break
    
    # If we get here, all retries failed
    print(f"ERROR: Failed to generate image using imagen model: {last_exception}")
    print(f"Error type: {type(last_exception).__name__}")
    print(f"\nNote: Image generation with Gemini requires:")
    print(f"  1. Access to Imagen API (configured model: {GEMINI_IMAGE_MODEL})")
    print(f"  2. Proper API key with image generation permissions")
    print(f"  3. Updated google-generativeai library (>=0.8.0)")
    print(f"\nThe art concept prompt has been saved to the gist.")
    print(f"You can use it with other image generation tools:")
    print(f"  - DALL-E (OpenAI)")
    print(f"  - Stable Diffusion")
    print(f"  - Midjourney")
    print(f"  - Vertex AI Imagen (Google Cloud)")
    raise ImageGenerationError(f"Image generation failed: {last_exception}")


def create_metadata_file(art_style, art_concept, gist_url, image_path):
    """
    Create a metadata JSON file with generation details.
    
    Args:
        art_style: The art style used
        art_concept: The art concept prompt
        gist_url: URL to the gist containing the prompt
        image_path: Path to the generated image
    """
    metadata = {
        "art_style": art_style,
        "art_concept": art_concept,
        "gist_url": gist_url,
        "image_file": Path(image_path).name,
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC"),
        "gemini_model": GEMINI_MODEL
    }
    
    metadata_filename = Path(image_path).stem + "_metadata.json"
    metadata_path = IMAGES_DIR / metadata_filename
    
    with open(metadata_path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)
    
    print(f"✓ Metadata saved to {metadata_path}")


def main():
    """Main execution function."""
    print("=" * 60)
    print("Art Style Image Generator")
    print("=" * 60)
    
    # Validate environment variables
    if not GEMINI_API_KEY:
        print("ERROR: GEMINI_API_KEY environment variable is not set")
        sys.exit(1)
    
    # Step 1: Select random art style
    art_style = select_random_art_style()
    print(f"\n[1/4] Selected art style: {art_style}")
    
    # Step 2: Generate detailed art concept
    art_concept = generate_art_concept(art_style)
    print(f"\n[2/4] Generated art concept:")
    print(f"  {art_concept[:150]}...")
    
    # Step 3: Save prompt to gist
    gist_url = save_prompt_to_gist(art_style, art_concept)
    print(f"\n[3/4] Saved to gist: {gist_url}")
    
    # Step 4: Generate image (optional based on configuration)
    image_path = None
    if SKIP_IMAGE_GENERATION:
        print(f"\n[4/4] Skipping image generation (SKIP_IMAGE_GENERATION=true)")
        print("  Note: Image generation requires Imagen API access")
    else:
        print(f"\n[4/4] Generating image...")
        try:
            image_path = generate_image(art_concept, art_style)
            print(f"  Image saved: {image_path}")
            
            # Create metadata file
            create_metadata_file(art_style, art_concept, gist_url, image_path)
        except ImageGenerationError as e:
            print(f"\n⚠️  Image generation failed: {e}")
            print("  The art concept has been saved to the gist and can be used")
            print("  with other image generation tools.")
            image_path = None
    
    print("\n" + "=" * 60)
    print("✓ Art generation complete!")
    print(f"  Art Style: {art_style}")
    print(f"  Prompt: {gist_url}")
    if image_path:
        print(f"  Image: {image_path}")
    else:
        print(f"  Image: Not generated (use prompt with external tools)")
    print("=" * 60)
    
    # Return success even if image generation failed
    # The main value is in the art concept generation and gist storage
    sys.exit(0)


if __name__ == "__main__":
    main()
