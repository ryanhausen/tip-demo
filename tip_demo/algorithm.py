from itertools import chain, filterfalse
from typing import Callable, List, Optional


import networkx as nx

try:
    from tip_demo.algorithm_data_model import Author, Paper
except ImportError:
    from algorithm_data_model import Author, Paper

GraphEvalFunction = Callable[[nx.Graph, nx.Graph, Optional[List[nx.Graph]]], nx.Graph]


def convert_paper_to_graph(authors: List[Author], paper: Paper) -> nx.Graph:

    g = nx.Graph()
    g.add_node(paper.node_id, **paper.node_attrs)
    for author in authors:
        g.add_node(author.node_id, **author.node_attrs)
        g.add_edge(author.node_id, paper.node_id)

    return g


def evaluate_graphs_authors(
    seed_graph: nx.Graph,
    target_graph: nx.Graph,
    peripheral_graphs: Optional[List[nx.Graph]] = [],
) -> nx.Graph:

    # get the authors from the seed graph that are in the target graph
    is_author = lambda node: node[1]["type"] == "author"
    is_seed = lambda node: node[0] in seed_graph.nodes()

    seed_authors = list(map(
        lambda node: (node[0], seed_graph.nodes[node[0]]),
        filter(
            lambda node: is_author(node) and is_seed(node),
            target_graph.nodes(data=True)
        )
    ))

    if len(seed_authors) == 0:
        print("No seed authors found")
        return target_graph

    non_seed_authors = list(filter(
        lambda node: is_author(node) and not is_seed(node),
        target_graph.nodes(data=True)
    ))

    # assign scores to the non seed authors based on the number and scores of the seed authors
    seed_score = sum(map(lambda node: node[1]["ai_score"], seed_authors)) / len(
        seed_authors
    )

    if len(non_seed_authors) == 0:
        print("No non seed authors found")
        return target_graph
    else:
        non_seed_score = seed_score / len(non_seed_authors) if len(non_seed_authors) > 0 else 0

    for author in non_seed_authors:
        author[1]["ai_score"] = non_seed_score

    G = nx.Graph()

    paper = next(
        filter(lambda node: node[1]["type"] == "paper", target_graph.nodes(data=True))
    )

    G.add_node(paper[0], **paper[1])
    for author in chain.from_iterable([non_seed_authors, seed_authors]):
        G.add_node(author[0], **author[1])
        G.add_edge(author[0], paper[0])

    return G


def evaluate_graphs_papers(
    seed_graph: nx.Graph,
    target_graph: nx.Graph,
    peripheral_graphs: Optional[List[nx.Graph]] = [],
) -> nx.Graph:

    return target_graph


def evaluate_graph(
    seed_graph: nx.Graph,
    target_graph: nx.Graph,
    peripheral_graphs: Optional[List[nx.Graph]] = [],
    eval_graph_author_fn: GraphEvalFunction = evaluate_graphs_authors,
    eval_graph_paper_fn: GraphEvalFunction = evaluate_graphs_papers,
    λ_author: float = 0.5,
    λ_paper: float = 0.5,
) -> nx.Graph:

    author_scored_graph = eval_graph_author_fn(
        seed_graph, target_graph, peripheral_graphs
    )

    paper_scored_graph = eval_graph_paper_fn(
        seed_graph, target_graph, peripheral_graphs
    )

    return combine_author_paper_scores(
        author_scored_graph,
        paper_scored_graph,
        λ_author,
        λ_paper,
    )


def combine_author_paper_scores(
    author_scored_graph: nx.Graph,
    paper_scored_graph: nx.Graph,
    λ_author: float = 0.5,
    λ_paper: float = 0.5,
) -> nx.Graph:
    G = nx.Graph()

    for node in author_scored_graph.nodes(data=True):
        author_score = node[1]["ai_score"] * λ_author
        paper_score = paper_scored_graph.nodes[node[0]]["ai_score"] * λ_paper
        score = author_score + paper_score
        node[1]["ai_score"] = score
        G.add_node(node[0], **node[1])

    for edge in author_scored_graph.edges(data=True):
        G.add_edge(edge[0], edge[1], **edge[2])

    return G


if __name__ == "__main__":
    authors = [
        Author(1, "Smith", "John", "A", 1.0),
        Author(2, "Smith", "Jane", "B", 1.0),
        Author(3, "Smith", "James", "C", 1.0),
    ]
    paper = Paper(1, "A paper")

    seed_graph = convert_paper_to_graph(authors, paper)

    authors = [
        Author(1, "Smith", "John", "A"),
        Author(2, "Smith", "Jane", "B"),
        Author(4, "AAABM", "Craig", "C"),
        Author(5, "AFDK", "Vince", "C"),
    ]
    paper = Paper(2, "A new paper")

    target_graph = convert_paper_to_graph(authors, paper)

    updated_target_graph = evaluate_graph(
        seed_graph,
        target_graph,
        λ_author=1.0,
        λ_paper=0.0,
    )



    list(map(print, updated_target_graph.nodes(data=True)))
