"""
Simple Git practice file plus a tiny news wordcloud demo.
Requires: pip install requests beautifulsoup4 wordcloud matplotlib
"""

import re
from pathlib import Path
from typing import List

import requests
from bs4 import BeautifulSoup
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt

# A small list of public news pages to crawl.
# Replace or extend these with sources you are allowed to scrape.
NEWS_URLS = [
    "https://news.ycombinator.com/",
    "https://www.bbc.com/news",
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; WordCloudBot/1.0)",
}


def fetch_url(url: str, timeout: int = 10) -> str:
    resp = requests.get(url, headers=HEADERS, timeout=timeout)
    resp.raise_for_status()
    return resp.text


def extract_text(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()
    chunks = []
    for tag in soup.find_all(["h1", "h2", "h3", "p", "a"]):
        text = tag.get_text(" ", strip=True)
        if text:
            chunks.append(text)
    text = " ".join(chunks)
    return re.sub(r"\s+", " ", text).strip()


def build_corpus(urls: List[str]) -> str:
    parts = []
    for url in urls:
        try:
            html = fetch_url(url)
            parts.append(extract_text(html))
        except Exception as exc:
            print(f"Skip {url}: {exc}")
    return " ".join(parts)


def create_wordcloud(text: str, output_path: Path) -> None:
    if not text:
        print("No text collected. Nothing to render.")
        return
    wc = WordCloud(
        width=1600,
        height=900,
        background_color="white",
        stopwords=STOPWORDS,
        collocations=False,
    ).generate(text)
    wc.to_file(str(output_path))
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    plt.tight_layout()
    plt.show()


def main() -> None:
    print("Hello, this is a test file for git and github.")
    print("I am learning how to use git and github to manage my code and collaborate with others.")
    print("I will create a repository on github and push this file to it.")
    print("I will also create a branch and make some changes to this file, and then merge it back to the main branch.")
    while True:
        if input("Do you want to continue learning git and github? (yes/no) ").strip().lower() == "no":
            break
    print("Thank you for learning git and github with me. Goodbye!")

    if input("Generate a morning news wordcloud now? (yes/no) ").strip().lower() == "yes":
        corpus = build_corpus(NEWS_URLS)
        output_file = Path("morning_news_wordcloud.png")
        create_wordcloud(corpus, output_file)
        print(f"Saved wordcloud to {output_file.resolve()}")


if __name__ == "__main__":
    main()
