from typing import Annotated

import typer
from rich import print

from city_mail.delivery_optimizer.addresses_data_adapter import (
    NominatimAddressesDataDownloader,
)
from city_mail.utils.file_path_utils import urlify
from city_mail.navigation.graph_path_navigator import GraphPathNavigator
from city_mail.delivery_optimizer.osm_streets_graph_adapter import (
    OsmStreetsGraphDownloader,
)
from city_mail.delivery_optimizer.path_optimizer_service import PathOptimizer
from city_mail.utils.visualization_utils import save_shortest_delivery_path_map


app = typer.Typer()


def display_navigation(
    navigator: GraphPathNavigator,
    path: list[int],
    delivery_addresses_to_nodes: dict[str, int],
) -> None:
    _path = path.copy()
    _delivery_addresses_to_nodes = delivery_addresses_to_nodes.copy()
    starting_address, starting_node = next(iter(_delivery_addresses_to_nodes.items()))
    del _delivery_addresses_to_nodes[starting_address]

    print(f":house: [green]Start from[/green] [italic]{starting_address}[/italic]")
    for street in navigator.navigate(_path):
        deliveries_in_street = [
            addr
            for addr, node in _delivery_addresses_to_nodes.items()
            if node in street.node_ids
        ]
        for addr in deliveries_in_street:
            del _delivery_addresses_to_nodes[addr]
            print(f":package: [green]Deliver to[/green] [italic]{addr}[/italic]")
        else:
            print(f":right_arrow: Follow {street.name} for {street.length:.0f} meters")
    print(":house: [green]Navigation complete.[/green]")


@app.command()
def main(
    city: str,
    addresses_file_path: Annotated[
        str,
        typer.Option(help="File containing a list of addresses for the chosen city"),
    ] = "addresses_files/varese.txt",
    best_route_folder: Annotated[
        str,
        typer.Option(help="Folder where save the maps with the optimized street path"),
    ] = "shortest_delivery_maps",
) -> None:
    osm_street_graph = OsmStreetsGraphDownloader(city)
    path_optimizer = PathOptimizer(
        streets_graph_adapter=osm_street_graph,
        address_data_adapter=NominatimAddressesDataDownloader(),
    )

    with open(addresses_file_path) as f:
        addresses = f.read().splitlines()

    print(
        "[green]Calculating the shortest path for the provided deliveries addresses. Could take a while...[/green]"
    )
    best_route, delivery_addresses_to_nodes, starting_node = (
        path_optimizer.calculate_shortest_path(addresses)
    )

    display_navigation(
        GraphPathNavigator(osm_street_graph.city_graph),
        best_route,
        delivery_addresses_to_nodes,
    )

    save_shortest_delivery_path_map(
        osm_street_graph.city_graph,
        best_route,
        starting_node,
        delivery_addresses_to_nodes.values(),
        f"{best_route_folder}/{urlify(city)}.png",
    )


if __name__ == "__main__":
    app()
