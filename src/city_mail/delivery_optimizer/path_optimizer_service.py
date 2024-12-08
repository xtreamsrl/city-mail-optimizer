import logging
from typing import Protocol

import networkx as nx
from networkx.algorithms.approximation.traveling_salesman import (
    traveling_salesman_problem,
)

from city_mail.delivery_optimizer.addresses_data_adapter import AbstractAddressesData
from city_mail.delivery_optimizer.osm_streets_graph_adapter import AbstractStreetsGraph


class AbstractPathOptimizer(Protocol):
    def calculate_shortest_path(
        self, addresses: list[str]
    ) -> tuple[list[int], dict[str, int], int]: ...


class PathOptimizer(AbstractPathOptimizer):
    def __init__(
        self,
        streets_graph_adapter: AbstractStreetsGraph,
        address_data_adapter: AbstractAddressesData,
    ):
        self.streets_graph_adapter = streets_graph_adapter
        self.address_data_adapter = address_data_adapter

    def calculate_shortest_path(
        self, addresses: list[str]
    ) -> tuple[list[int], dict[str, int], int]:
        # TODO: too much responsibility?
        delivery_addresses_data = self.address_data_adapter.get_multiple_addresses_data(
            addresses
        )
        delivery_nodes = [
            self.streets_graph_adapter.closest_node_id_from_address(address_data)
            for address_data in delivery_addresses_data
        ]

        delivery_addresses_to_nodes = dict(zip(addresses, delivery_nodes))

        starting_node = delivery_nodes[0]

        logging.info(
            f"Calculating the shortest path using TSP for delivery nodes {delivery_nodes}"
        )
        best_route = traveling_salesman_problem(
            self.streets_graph_adapter.city_graph,
            nodes=delivery_nodes,
            weight="travel_time",
            cycle=True,
            method=nx.approximation.simulated_annealing_tsp,
            init_cycle="greedy",
            seed=1,
        )

        return best_route, delivery_addresses_to_nodes, starting_node
