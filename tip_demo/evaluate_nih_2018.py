import json
from typing import List, Union
import matplotlib.pyplot as plt
import networkx as nx
import os

from tqdm import tqdm

from nih_award import NihAward
from nih_pi import NihPi


try:
    from tip_demo.algorithm_data_model import Author, Paper
    from tip_demo.algorithm import convert_paper_to_graph, evaluate_graph
    root_path = "tip_demo"
except ImportError:
    from algorithm_data_model import Author, Paper
    from algorithm import convert_paper_to_graph, evaluate_graph
    root_path = ""

with_root = lambda path: os.path.join(root_path, path)

def get_stored_graph(year:int, compose:bool=True, is_seed:bool=True) -> Union[nx.Graph, List[nx.Graph]]:

    if os.path.exists(with_root("composed_graph_{year}.gexf")):
        return nx.read_gexf(with_root(f"composed_graph_{year}.gexf"))
    else:
        ml_authors = []
        with open(with_root(f"pis-{year}.json"), "r") as f:
            ml_authors.extend(list(map(NihPi.from_nih_api, json.load(f))))

        ml_awards = []
        with open(with_root(f"awards-{year}.json"), "r") as f:
            ml_awards.extend(list(map(NihAward.from_nih_api, json.load(f))))

        ai_score = {"ai_score": 1.0} if is_seed else {}

        ml_authors = dict(map(
            lambda x: (x.profile_id, x.to_graph_object(ai_score)),
            set(ml_authors)
        ))

        get_authors = lambda ids: [ml_authors[i] for i in ids]

        paper_graphs = list(
            map(
                lambda award: convert_paper_to_graph(
                    get_authors(award.principal_investigators),
                    award.to_graph_object()
                ),
                set(ml_awards)
            )
        )

        print(f"Found {len(paper_graphs)} papers")
        print("total nodes:", sum(map(nx.number_of_nodes, paper_graphs)))

        if compose:
            composed_graph = nx.compose_all(paper_graphs)
            print("composed nodes:", nx.number_of_nodes(composed_graph))

            nx.write_gexf(composed_graph, with_root(f"composed_graph_{year}.gexf"))
            return composed_graph
        else:
            return paper_graphs


def main():

    print("Loading 2019 graph")
    label_graph_2019 = get_stored_graph(2019)
    print("Loading 2020 graph")
    label_graph_2020 = get_stored_graph(2020)

    paper_graphs_2018 = get_stored_graph(2018, compose=False, is_seed=False)

    if os.path.exists("label_graph_2019_2020.gexf"):
        seed_graph = nx.read_gexf(with_root("label_graph_2019_2020.gexf"))
    else:
        print("Composing 2019 and 2020 graphs")
        seed_graph = nx.compose(label_graph_2019, label_graph_2020)
        print("Saving composed graph")
        nx.write_gexf(seed_graph, with_root("label_graph_2019_2020.gexf"))

    print("Evaluating graph")




    for paper_graph in tqdm(paper_graphs_2018):
        out_graph = evaluate_graph(seed_graph, paper_graph, λ_author=1.0, λ_paper=0.0)
        if any(map(lambda n: n[1]["ai_score"] > 0, out_graph.nodes(data=True))):
            f, ax = plt.subplots(figsize=(8, 8))

            ax.set_title(next(filter(
                lambda node: node[1]["type"]=="paper",
                out_graph.nodes(data=True)
            ))[1]["title"])

            nx.draw(
                out_graph,
                ax=ax,
                font_size=10,
                node_size=300,
                labels = {n[0]: n[1]["ai_score"] if n[1]["type"]=="author" else "" for n in out_graph.nodes(data=True)},
                with_labels=True,
                node_color=[n[1]["color"] for n in out_graph.nodes(data=True)],
            )
            plt.show()

if __name__ == "__main__":
    main()


