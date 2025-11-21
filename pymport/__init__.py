import shutil
import tempfile
from pathlib import Path

from pymport import converters, files, parser, tools


def create_graph(lib_path: str, workdir: Path = Path(".")) -> Path:
    lib = Path(lib_path)
    out = workdir / f"{lib.name}.gml"
    workdir.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)

        new_lib, inits = files.create_inits(lib=lib, workdir=tmp)
        dot_file = converters.create_pydeps(lib_path=new_lib, workdir=tmp)
        gml = converters.dot2gml(dot=dot_file, workdir=tmp)

        graph = parser.Graph.load(file=gml)
        clustered = tools.clusterize(g=graph)
        colored = tools.colorize(clustered)
        pruned = tools.prune(colored, inits)

        save_file = tmp / out.name
        pruned.save(file=save_file)
        shutil.copy(src=save_file, dst=out)
    return out
