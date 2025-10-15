import re
import tarfile
import time
from contextlib import ExitStack
from functools import cached_property
from tempfile import TemporaryDirectory
from typing import Optional
from urllib.error import HTTPError

import arxiv
import requests
import tiktoken
from llm import get_llm
from loguru import logger
from requests.adapters import HTTPAdapter, Retry


class ArxivPaper:
    def __init__(self, paper: arxiv.Result):
        self._paper = paper
        self.score = None

    @property
    def title(self) -> str:
        return self._paper.title

    @property
    def summary(self) -> str:
        return self._paper.summary

    @property
    def authors(self) -> list[str]:
        return self._paper.authors

    @cached_property
    def arxiv_id(self) -> str:
        return re.sub(r"v\d+$", "", self._paper.get_short_id())

    @property
    def pdf_url(self) -> str:
        return self._paper.pdf_url

    @cached_property
    def code_url(self) -> Optional[str]:
        s = requests.Session()
        retries = Retry(total=5, backoff_factor=0.1)
        s.mount("https://", HTTPAdapter(max_retries=retries))
        try:
            paper_list = s.get(
                f"https://paperswithcode.com/api/v1/papers/?arxiv_id={self.arxiv_id}"
            ).json()
        except Exception as e:
            logger.debug(f"Error when searching {self.arxiv_id}: {e}")
            return None

        if paper_list.get("count", 0) == 0:
            return None
        paper_id = paper_list["results"][0]["id"]

        try:
            repo_list = s.get(
                f"https://paperswithcode.com/api/v1/papers/{paper_id}/repositories/"
            ).json()
        except Exception as e:
            logger.debug(f"Error when searching {self.arxiv_id}: {e}")
            return None
        if repo_list.get("count", 0) == 0:
            return None
        return repo_list["results"][0]["url"]
