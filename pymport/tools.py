import collections
import colorsys

from pymport import parser


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
    colors_len = max(n.label.count(".") if n.label else 0 for n in g.nodes) + 1
    color_map = _get_colormap(colors_len)
    m = 0
    g = g.model_copy(deep=True)
    for n in g.nodes:
        level = n.label.count(".") if n.label else 0
        m = max([level, m])
        if n.graphics:
            n.graphics.fill = f'"{color_map[level]}"'
    return g


def prune(g: parser.Graph, prune_names: list[str]):
    g = g.model_copy(deep=True)
    prune_ids = [i.id for i in g.nodes if i.norm_name in prune_names]

    entries = []
    for i in g.entries.copy():
        drop = False
        if isinstance(i, parser.Node) and (i.id in prune_ids):
            drop = True

        if isinstance(i, parser.Edge) and (
            (i.source in prune_ids) or (i.target in prune_ids)
        ):
            drop = True

        if not drop:
            entries.append(i)
    g.entries = entries
    return g


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
                name=f'"{group}"',
                label=f'"{group}"',
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


def _get_colormap(n: int) -> list[str]:
    HSV_tuples = [(x / n * 0.8, 1, 1) for x in range(n)]
    RGB_tuples = [colorsys.hsv_to_rgb(*x) for x in HSV_tuples]
    return [
        f"#{int(255*r):02X}{int(255*g):02X}{int(255*b):02X}" for r, g, b in RGB_tuples
    ]
