import os
import requests
import openai
from flask import Flask, render_template
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

NEWSAPI_KEY = os.getenv("NEWSAPI_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

NEWS_ENDPOINT = "https://newsapi.org/v2/top-headlines"


def fetch_headlines():
    params = {
        "apiKey": NEWSAPI_KEY,
        "language": "en",
        "pageSize": 5,
    }
    resp = requests.get(NEWS_ENDPOINT, params=params, timeout=10)
    resp.raise_for_status()
    data = resp.json()
    return data.get("articles", [])


def summarize(text):
    prompt = f"Summarize the following news article in 1-2 sentences:\n\n{text}"
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # adjust as needed
        messages=[{"role": "user", "content": prompt}],
        max_tokens=60,
    )
    return response.choices[0].message.content.strip()


@app.route("/")
def index():
    articles = []
    if not NEWSAPI_KEY or not OPENAI_API_KEY:
        return "Missing API keys. Please set NEWSAPI_KEY and OPENAI_API_KEY."

    for item in fetch_headlines():
        description = item.get("description") or ""
        summary = summarize(description)
        articles.append({
            "title": item.get("title"),
            "url": item.get("url"),
            "summary": summary,
        })

    return render_template("index.html", articles=articles)


if __name__ == "__main__":
    app.run(debug=True)
