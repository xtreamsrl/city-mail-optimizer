import logging
from typing import Protocol

import networkx as nx
from networkx.algorithms.approximation.traveling_salesman import traveling_salesman_problem

from src.city_mail.addresses_data_adapter import AddressesDataPort
from src.city_mail.osm_streets_graph_adapter import StreetsGraphPort


class PathOptimizerPort(Protocol):
    def calculate_shortest_path(self, addresses: list[str]) -> tuple[list[int], list[int], int]:
        ...


class PathOptimizerApplication(PathOptimizerPort):
    def __init__(self,
                 streets_graph_adapter: StreetsGraphPort,
                 address_data_adapter: AddressesDataPort):
        self.streets_graph_adapter = streets_graph_adapter
        self.address_data_adapter = address_data_adapter

    def calculate_shortest_path(self, addresses: list[str]) -> tuple[list[int], list[int], int]:
        delivery_addresses_data = self.address_data_adapter.get_multiple_addresses_data(addresses)
        delivery_nodes = [self.streets_graph_adapter.closest_node_id_from_address(address_data)
                          for address_data in delivery_addresses_data]
        starting_node = delivery_nodes[0]

        logging.info(f"Calculating the shortest path using TSP for delivery nodes {delivery_nodes}")
        best_route = traveling_salesman_problem(
            self.streets_graph_adapter.city_graph,
            nodes=delivery_nodes,
            weight="travel_time",
            cycle=True,
            method=nx.approximation.simulated_annealing_tsp,
            init_cycle="greedy",
            seed=1,
        )

        logging.info(f"Reordering best route")
        best_route = self._reorder_route(best_route, starting_node)
        
        return best_route, delivery_nodes, starting_node

    def _reorder_route(self, route: list[int], starting_node: int) -> list[int]:
        return (
                route[route.index(starting_node): -1]
                + route[: route.index(starting_node)]
                + [starting_node]
        )