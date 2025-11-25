#!/usr/bin/env python3
"""
Art Style Prompt Generator
Picks an art style, generates a detailed art concept using Gemini,
and saves the prompt to a public gist for display in the UI.
"""

import os
import sys
import json
import random
from datetime import datetime, timezone
from pathlib import Path

import google.generativeai as genai
from github import Github, Auth, InputFileContent


# Configuration
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
GEMINI_MODEL = os.environ.get("GEMINI_MODEL", "gemini-2.0-flash-exp")
GIST_TOKEN = os.environ.get("GIST_TOKEN")
FISH_GIST_ID = os.environ.get("FISH_GIST_ID")

# Paths
SCRIPT_DIR = Path(__file__).parent
REPO_ROOT = SCRIPT_DIR.parent
ART_STYLES_FILE = REPO_ROOT / "art_styles.json"

# Gist filename for storing all prompts
PROMPTS_GIST_FILENAME = "art_prompts.json"


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
    Save the art concept prompt to a public GitHub Gist as a JSON file.
    The JSON file contains all prompts and can be fetched by the UI.
    
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
        
        # Get existing gist
        try:
            gist = g.get_gist(FISH_GIST_ID)
            print(f"Found existing gist: {FISH_GIST_ID}")
        except Exception as e:
            print(f"ERROR: Could not access gist {FISH_GIST_ID}: {e}")
            sys.exit(1)
        
        # Load existing prompts from gist if the file exists
        existing_prompts = []
        if PROMPTS_GIST_FILENAME in gist.files:
            try:
                existing_content = gist.files[PROMPTS_GIST_FILENAME].content
                existing_prompts = json.loads(existing_content)
                print(f"Loaded {len(existing_prompts)} existing prompts from gist")
            except (json.JSONDecodeError, Exception) as e:
                print(f"Warning: Could not parse existing prompts: {e}")
                existing_prompts = []
        
        # Create new prompt entry
        now_utc = datetime.now(timezone.utc)
        new_prompt = {
            "id": now_utc.strftime("%Y%m%d%H%M%S"),
            "art_style": art_style,
            "prompt": art_concept,
            "generated_at": now_utc.strftime("%Y-%m-%d %H:%M:%S UTC")
        }
        
        # Add new prompt to the beginning of the list
        existing_prompts.insert(0, new_prompt)
        
        # Update gist with JSON content
        print(f"Saving prompts to gist as {PROMPTS_GIST_FILENAME}...")
        json_content = json.dumps(existing_prompts, indent=2)
        files = {PROMPTS_GIST_FILENAME: InputFileContent(json_content)}
        gist.edit(files=files)
        
        gist_url = f"https://gist.github.com/{user.login}/{FISH_GIST_ID}"
        print(f"✓ Prompt saved to gist: {gist_url}")
        
        return gist_url
    except Exception as e:
        print(f"ERROR: Failed to save prompt to gist: {e}")
        sys.exit(1)


def main():
    """Main execution function."""
    print("=" * 60)
    print("Art Style Prompt Generator")
    print("=" * 60)
    
    # Validate environment variables
    if not GEMINI_API_KEY:
        print("ERROR: GEMINI_API_KEY environment variable is not set")
        sys.exit(1)
    
    # Step 1: Select random art style
    art_style = select_random_art_style()
    print(f"\n[1/3] Selected art style: {art_style}")
    
    # Step 2: Generate detailed art concept
    art_concept = generate_art_concept(art_style)
    print(f"\n[2/3] Generated art concept:")
    print(f"  {art_concept[:150]}...")
    
    # Step 3: Save prompt to gist
    gist_url = save_prompt_to_gist(art_style, art_concept)
    print(f"\n[3/3] Saved to gist: {gist_url}")
    
    print("\n" + "=" * 60)
    print("✓ Prompt generation complete!")
    print(f"  Art Style: {art_style}")
    print(f"  Gist URL: {gist_url}")
    print("=" * 60)
    
    sys.exit(0)


if __name__ == "__main__":
    main()
