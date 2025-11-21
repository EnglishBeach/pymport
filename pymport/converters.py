import subprocess
from pathlib import Path


def create_pydeps(lib_path: Path, workdir: Path) -> Path:
    out = workdir / "out.dot"
    cmd = f'pydeps "{lib_path.resolve()}" --dot-output "{out.name}" --show-dot --noshow --include-missing --only {lib_path.stem}'
    sp = subprocess.run(
        cmd,
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
    cmd = f'gv2gml -o "{out.name}" "{dot.resolve()}"'
    print(cmd)
    sp = subprocess.run(
        cmd,
        shell=True,
        cwd=workdir,
        capture_output=True,
        check=False,
    )
    if sp.returncode:
        raise RuntimeError("\n" + sp.stderr.decode())
    return out
