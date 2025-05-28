#!/bin/bash
cd "$(dirname "$0")/"
export GEMINI_API_KEY=$GEMINI_API_KEY
uv run server.py 