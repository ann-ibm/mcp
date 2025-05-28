from typing import Any
from google import genai
from google.genai import types
from io import BytesIO
import os
import uuid
from PIL import Image
import sys
import json
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import uvicorn

app = FastAPI()

print("GEMINI_API_KEY:", os.getenv('GEMINI_API_KEY'), file=sys.stderr)

def generate_image_from_gemini(prompt: str) -> str:
    print("Starting image generation with Gemini...\n", file=sys.stderr)
    api_key = os.getenv('GEMINI_API_KEY')
    print(f"Debug: Using API key: {api_key[:10]}...", file=sys.stderr)
    client = genai.Client(api_key=api_key)
    contents = (prompt)
    print(f"Debug: Sending prompt to Gemini: {prompt}", file=sys.stderr)
    response = client.models.generate_content(
        model="gemini-2.0-flash-exp-image-generation",
        contents=contents,
        config=types.GenerateContentConfig(
            response_modalities=['Text', 'Image']
        )
    )
    print("Debug: Got response from Gemini", file=sys.stderr)
    print(f"Debug: Raw response: {response}", file=sys.stderr)
    
    if not response or not response.candidates:
        print("Debug: No response from Gemini", file=sys.stderr)
        return "No response from Gemini"
        
    for part in response.candidates[0].content.parts:
        if part.text is not None:
            print(f"Debug: Got text response: {part.text}", file=sys.stderr)
            sys.stderr.write(part.text + '\n')
        elif part.inline_data is not None:
            print("Debug: Got image data", file=sys.stderr)
            image = Image.open(BytesIO((part.inline_data.data)))
            # Create generated-images directory if it doesn't exist
            if not os.path.exists('generated-images'):
                os.makedirs('generated-images')
            # Generate unique filename
            unique_filename = f"generated-images/{uuid.uuid4()}.png"
            image.save(unique_filename)
            print(f"Debug: Saved image to {unique_filename}", file=sys.stderr)
            return os.path.abspath(unique_filename)
    print("Debug: No valid image data found", file=sys.stderr)
    return "No valid image data found."

@app.post("/generate")
async def generate_image(request: dict):
    try:
        prompt = request.get("prompt")
        if not prompt:
            raise HTTPException(status_code=400, detail="Prompt is required")
        
        result = generate_image_from_gemini(prompt)
        return JSONResponse(content={"image_path": result})
    except Exception as e:
        print(f"Error generating image: {e}", file=sys.stderr)
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)