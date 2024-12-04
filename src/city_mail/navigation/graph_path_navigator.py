from typing import Generator

import networkx as nx
from pydantic import BaseModel


class NavigationStreet(BaseModel):
    name: str
    length: float
    starting_node_id: int
    ending_node_id: int


class GraphPathNavigator:
    def __init__(self, graph: nx.Graph):
        self._graph = graph

    def navigate(self, path: list[int]) -> Generator[NavigationStreet, None, None]:
        current_name = None
        current_length = 0.0
        starting_node_id = path[0]

        for i in range(len(path) - 1):
            current_node = path[i]
            next_node = path[i + 1]
            edge_data = self._graph.get_edge_data(current_node, next_node)[0]
            edge_name = edge_data.get("name", edge_data.get("ref", "Unknown"))
            edge_length = edge_data["length"]

            # TODO: some edge contains multiple street names, understand better why this case happen in the graph edges
            if isinstance(edge_name, list):
                edge_name = edge_name[0]

            if current_name is None:
                current_name = edge_name

            if edge_name == current_name:
                current_length += edge_length
            else:
                yield NavigationStreet(
                    name=current_name,
                    length=current_length,
                    starting_node_id=starting_node_id,
                    ending_node_id=current_node,
                )
                current_name = edge_name
                current_length = 0
                starting_node_id = next_node

        yield NavigationStreet(
            name=current_name,
            length=current_length,
            starting_node_id=starting_node_id,
            ending_node_id=path[-1],
        )
