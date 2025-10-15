import arxiv
import feedparser
from tqdm import tqdm

from .paper import ArxivPaper


def get_arxiv_paper(query: str) -> list[ArxivPaper]:
    # Get and parse rss feed
    feed = feedparser.parse(f"https://rss.arxiv.org/atom/{query}")
    if "Feed error for query" in feed.feed.title:
        raise Exception(f"Invalid arxiv query: {query}")
    all_paper_ids = [
        i.id.removeprefix("oai:arXiv.org:")
        for i in feed.entries
        if i.arxiv_announce_type == "new"
    ]

    # Search for new papers
    client = arxiv.Client(num_retries=10, delay_seconds=10)
    bar = tqdm(total=len(all_paper_ids), desc="Retrieving arxiv papers")

    papers = []
    for i in range(0, len(all_paper_ids), 50):
        search = arxiv.Search(id_list=all_paper_ids[i : i + 50])
        batch = [ArxivPaper(p) for p in client.results(search)]
        bar.update(len(batch))
        papers.extend(batch)

    bar.close()
    return papers
