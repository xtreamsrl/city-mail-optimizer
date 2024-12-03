import networkx as nx
import osmnx as ox


def save_shortest_delivery_path_map(
    graph: nx.Graph,
    best_path: list[int],
    starting_node: int,
    delivery_nodes: list[int],
    saving_filepath: str,
) -> None:
    # TODO: add docstring
    ox.plot.plot_graph_route(
        graph,
        best_path,
        route_color="green",
        route_linewidth=4,
        route_alpha=0.5,
        orig_dest_size=4,
        node_color=[
            "blue" if n == starting_node else "red" if n in delivery_nodes else "white"
            for n in graph.nodes()
        ],
        node_alpha=[1 if n in delivery_nodes else 0.5 for n in graph.nodes()],
        node_size=[
            100 if n == starting_node else 50 if n in delivery_nodes else 20
            for n in graph.nodes()
        ],
        save=True,
        filepath=saving_filepath,
        dpi=3000,
        show=False,
    )
