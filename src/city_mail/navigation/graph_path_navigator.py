from typing import Generator

import networkx as nx
from pydantic import BaseModel


class NavigationStreet(BaseModel):
    name: str
    length: float
    node_ids: list[int]


class GraphPathNavigator:
    def __init__(self, graph: nx.Graph):
        self._graph = graph

    def navigate(self, path: list[int]) -> Generator[NavigationStreet, None, None]:
        # initialize the first street
        current_street_name = None
        current_street_length = 0.0
        current_street_node_ids = [path[0]]

        # iterate over edges in the path
        for i in range(len(path) - 1):
            # extract the nodes
            current_node = path[i]
            next_node = path[i + 1]
            current_edge_data = self._graph.get_edge_data(current_node, next_node)[0]
            current_edge_name = current_edge_data.get(
                "name", current_edge_data.get("ref", "Unknown")
            )
            current_edge_length = current_edge_data["length"]

            if isinstance(current_edge_name, list):
                # the edge may span multiple street names; in this case we keep the last one to start a new street
                current_edge_name = current_edge_name[-1]

            if current_street_name is None:
                # first street
                current_street_name = current_edge_name

            if current_edge_name == current_street_name:
                # still on the same street: update the length and add the node
                current_street_length += current_edge_length
                current_street_node_ids.append(next_node)
            else:
                # in a new street: yield the current one and start a new one
                yield NavigationStreet(
                    name=current_street_name,
                    length=current_street_length,
                    node_ids=current_street_node_ids,
                )
                # reset street attributes
                current_street_name = current_edge_name
                current_street_length = current_edge_length
                current_street_node_ids = [next_node]

        # yield the last street
        yield NavigationStreet(
            name=current_street_name,
            length=current_street_length,
            node_ids=current_street_node_ids,
        )
