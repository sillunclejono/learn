# Breaking News Aggregator

This demo shows how to build a simple breaking news aggregator that summarizes the latest headlines using an LLM. The web interface is intentionally styled like a 1990's blog for nostalgia.

## Setup

1. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Set the following environment variables:
   - `NEWSAPI_KEY`: API key from [NewsAPI](https://newsapi.org)
   - `OPENAI_API_KEY`: API key for OpenAI
3. Run the app:
   ```bash
   python app.py
   ```
4. Visit `http://localhost:5000` in your browser.

## Overview

The app fetches top headlines from NewsAPI, then asks an LLM to generate short summaries. The results are displayed on a single page with a vintage 90's blog appearance.
