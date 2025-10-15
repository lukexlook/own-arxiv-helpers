import re
from typing import Any

import arxiv


class ArxivPaper(object):

    def __init__(self, paper: arxiv.Result) -> None:
        self.title = paper.title
        self.authors = [au.name for au in paper.authors]
        self.summary = paper.summary

        self.arxiv_id = re.sub(r"v\d+$", "", paper.get_short_id())
        self.pdf_url = paper.pdf_url

        self.comment = paper.comment
        self.categories = paper.categories

    def as_dict(self) -> dict[str, Any]:
        return {
            "title": self.title,
            "authors": self.authors,
            "summary": self.summary,
            "arxiv_id": self.arxiv_id,
            "pdf_url": self.pdf_url,
            "comment": self.comment,
            "categories": self.categories,
        }
