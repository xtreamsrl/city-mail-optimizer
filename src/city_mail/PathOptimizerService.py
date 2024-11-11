from typing import Protocol

from networkx.algorithms.approximation.traveling_salesman import traveling_salesman_problem

from src.city_mail.OpenStreetMapGraphAdapter import StreetsGraphPort


class PathOptimizerPort(Protocol):
    def calculate_shortest_path(self, addresses: list[str]) -> list[str]:
        ...


class PathOptimizerApplication(PathOptimizerPort):
    def __init__(self, city: str, streets_graph: StreetsGraphPort):
        self._street_graph = streets_graph
        self._city_graph = self._street_graph.get_city_graph(city)

    def calculate_shortest_path(self, addresses: list[str]) -> list[str]:
        delivery_nodes = [self._street_graph.address_to_node_id(address) for address in addresses]

        best_route = traveling_salesman_problem(
            self._city_graph, nodes=delivery_nodes, cycle=True, method=None, seed=1
        )
        
        return [self._street_graph.node_id_to_address(node_id) for node_id in best_route]