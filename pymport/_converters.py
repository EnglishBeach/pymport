import subprocess
from pathlib import Path


def create_pydeps(lib_path: Path, workdir: Path) -> Path:
    out = workdir / "out.dot"
    sp = subprocess.run(
        f"pydeps {lib_path} --dot-output {out.name} --show-dot --noshow --include-missing --only {lib_path.stem}",
        shell=True,
        cwd=workdir,
        capture_output=True,
        check=False,
    )
    if sp.returncode:
        raise RuntimeError("\n" + sp.stderr.decode())
    return out


def dot2gml(dot: Path, workdir: Path) -> Path:
    out = workdir / "out.gml"
    sp = subprocess.run(
        f"gv2gml -o {out} {dot}",
        shell=True,
        cwd=workdir,
        capture_output=True,
        check=False,
    )
    if sp.returncode:
        raise RuntimeError("\n" + sp.stderr.decode())
    return out
