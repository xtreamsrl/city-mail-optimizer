from typing import Annotated

import typer
from rich import print

from city_mail.delivery_optimizer.addresses_data_adapter import (
    NominatimAddressesDataAdapter,
)
from city_mail.utils.file_path_utils import urlify
from city_mail.navigation.graph_path_navigator import GraphPathNavigator
from city_mail.delivery_optimizer.osm_streets_graph_adapter import (
    OsmStreetsGraphAdapter,
)
from city_mail.delivery_optimizer.path_optimizer_service import PathOptimizerApplication
from city_mail.utils.visualization_utils import save_shortest_delivery_path_map


app = typer.Typer()


def display_navigation(
    navigator: GraphPathNavigator,
    best_nodes: list[int],
    starting_node: int,
    delivery_nodes: dict[int, str],
) -> None:
    for street in navigator.navigate(best_nodes):
        if street.starting_node_id == starting_node:
            print(
                f":house: [green]Start from[/green] [italic]{delivery_nodes[street.starting_node_id]}[/italic]"
            )
            del delivery_nodes[street.starting_node_id]
        elif street.starting_node_id in delivery_nodes.keys():
            print(
                f":package: [green]Deliver to[/green] [italic]{delivery_nodes[street.starting_node_id]}[/italic]"
            )
            del delivery_nodes[street.starting_node_id]
        else:
            print(f":right_arrow: Follow {street.name} for {street.length:.0f} meters")


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
    osm_street_graph = OsmStreetsGraphAdapter(city)
    path_optimizer = PathOptimizerApplication(
        streets_graph_adapter=osm_street_graph,
        address_data_adapter=NominatimAddressesDataAdapter(),
    )

    with open(addresses_file_path) as f:
        addresses = f.read().splitlines()

    print(
        "[green]Calculating the shortest path for the provided deliveries addresses. Could take a while...[/green]"
    )
    best_route, delivery_nodes, starting_node = path_optimizer.calculate_shortest_path(
        addresses
    )

    display_navigation(
        GraphPathNavigator(osm_street_graph.city_graph),
        best_route,
        starting_node,
        delivery_nodes,
    )

    save_shortest_delivery_path_map(
        osm_street_graph.city_graph,
        best_route,
        starting_node,
        delivery_nodes.keys(),
        f"{best_route_folder}/{urlify(city)}.png",
    )


if __name__ == "__main__":
    main("Pavia, Pavia, Italia", "../../addresses.txt", "shortest_delivery_maps")
