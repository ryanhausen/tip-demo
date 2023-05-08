import dataclasses as dc
from typing import Any, Dict, List, Tuple

import networkx as nx

Node = Tuple[str, Dict[str, Any]]


@dc.dataclass
class Author:
    author_id: int
    last_name: str
    first_name: str
    middle_name: str = ""
    ai_score: float = 0.0
    color: str = "tab:blue"

    @property
    def node_id(self) -> str:
        return f"A:{self.author_id}"

    @property
    def node_attrs(self) -> Dict[str, Any]:
        return dict(
            type="author",
            last_name=self.last_name,
            first_name=self.first_name,
            middle_name=self.middle_name,
            ai_score=self.ai_score,
            color=self.color,
        )


@dc.dataclass
class Paper:
    paper_id: int
    title: str
    url: str = ""
    color: str = "tab:orange"
    ai_score: float = 0.0

    @property
    def node_id(self) -> str:
        return f"P:{self.paper_id}"

    @property
    def node_attrs(self) -> Dict[str, Any]:
        return dict(
            type="paper",
            title=self.title,
            url=self.url,
            color=self.color,
            ai_score=self.ai_score,
        )
