import collections
from pathlib import Path
from typing import Optional

from pydantic import BaseModel, model_validator

from pymport import parser


def _make_groups(
    nodes: list[parser.Node],
    level: int,
    max_id: int,
    cluster_volume: int = 1,
    external_gid: int | None = None,
) -> list[parser.Node]:
    groups = collections.defaultdict(lambda: [])
    add_nodes = []
    for n in nodes:
        titles = n.norm_name.split(".")
        if len(titles) < level + 1:
            continue
        else:
            groups[titles[level]].append(n)

    for i, (group, group_nodes) in enumerate(groups.items()):
        if len(group_nodes) > cluster_volume:
            gid = max_id + 1 + i
            node = parser.Node(
                isGroup=1,
                id=gid,
                name=f'"Group {group}"',
                label=f'"Group {group}"',
                gid=external_gid,
            )
            add_nodes.append(node)
            for n in group_nodes:
                n.gid = gid

            inner_clusters = _make_groups(
                group_nodes,
                level=level + 1,
                max_id=max_id + 1 + i,
                external_gid=gid,
            )
            max_id = max_id + 1 + i
            add_nodes.extend(inner_clusters)

    return add_nodes


def clusterize(g: parser.Graph):
    g = g.model_copy(deep=True)
    nodes = g.nodes
    clusters = _make_groups(
        nodes,
        level=1,
        max_id=len(nodes),
    )

    g.entries = clusters + g.entries
    return g


def colorize(g: parser.Graph):
    color_map = [
        "#0a0ee7c0",
        "#0ae7d1c0",
        "#0ae736c0",
        "#d8e70ac0",
        "#e78f0ac0",
        "#e70a0ac0",
    ]
    g = g.model_copy()
    for n in g.nodes:

        level = n.label.count(".") if n.label else 0
        if n.graphics:
            n.graphics.fill = f'"{color_map[level]}"'
    return g
