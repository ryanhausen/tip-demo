import json
import matplotlib.pyplot as plt
import networkx as nx

from nih_award import NihAward
from nih_pi import NihPi


try:
    from tip_demo.algorithm_data_model import Author, Paper
    from tip_demo.algorithm import convert_paper_to_graph
except ImportError:
    from algorithm_data_model import Author, Paper
    from algorithm import convert_paper_to_graph

def main():

    ml_authors = []
    with open("pis-2019.json", "r") as f:
        ml_authors.extend(list(map(NihPi.from_nih_api, json.load(f))))

    ml_awards = []
    with open("awards-2019.json", "r") as f:
        ml_awards.extend(list(map(NihAward.from_nih_api, json.load(f))))

    ml_authors = dict(map(
        lambda x: (x.profile_id, x.to_graph_object()),
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

    composed_graph = nx.compose_all(paper_graphs)
    print("composed nodes:", nx.number_of_nodes(composed_graph))


    f, ax = plt.subplots(figsize=(40, 40))
    nx.draw(
        composed_graph,
        ax=ax,
        font_size=6,
        node_size=10,
        with_labels=False,
        node_color=[n[1]["color"] for n in composed_graph.nodes(data=True)],
    )
    plt.show()

if __name__ == "__main__":
    main()


