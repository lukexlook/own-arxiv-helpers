import json
import sys

import arxiv
from tqdm import tqdm

sys.path.append("src")

from ruamel.yaml import YAML

from own_arxiv_helpers.paper import ArxivPaper

yaml = YAML(typ="safe")
with open("categories.yml") as fp:
    categories = set(yaml.load(fp))


if __name__ == "__main__":
    a = "2511.05491"
    b = "2511.07421"

    year_month = a.split(".")[0]
    assert year_month == b.split(".")[0]

    a_int = int(a.split(".")[-1])
    b_int = int(b.split(".")[-1])
    assert a_int < b_int

    all_paper_ids = [f"{year_month}.{c:05d}" for c in range(a_int + 1, b_int)]
    bar = tqdm(total=len(all_paper_ids), desc="Retrieving arxiv papers")
    client = arxiv.Client(num_retries=10, delay_seconds=10)

    papers: list[ArxivPaper] = []
    for i in range(0, len(all_paper_ids), 50):
        search = arxiv.Search(id_list=all_paper_ids[i : i + 50])
        batch = [ArxivPaper(p) for p in client.results(search)]
        bar.update(len(batch))

        batch = [p for p in batch if set(p.categories) & categories]
        papers.extend(batch)

    print(f"⏩ Papers for the fix ({len(papers)}):")
    for paper in papers:
        print(json.dumps(paper.as_dict()))
