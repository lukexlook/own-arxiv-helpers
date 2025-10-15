import json
import sys

sys.path.append("src")

from ruamel.yaml import YAML

from own_arxiv_helpers import get_arxiv_paper

if __name__ == "__main__":
    yaml = YAML(typ="safe")
    with open("categories.yml") as fp:
        categories = yaml.load(fp)
    query = "+".join(categories)
    papers = get_arxiv_paper(query)

    if len(papers) == 0:
        print("🍃 No papers found today! Have a good rest.")
    else:
        print("🔎 Your query:", query)
        print("⏩ Papers for you today:")
        for paper in papers:
            print(json.dumps(paper.as_dict()))
