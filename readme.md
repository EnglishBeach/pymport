# PyLibScheme

[RU Documentation](documentation/README.ru.md)

Graph drawing tool from Python library folder. Uses `pydeps` and `pyreverse` for graph file `.dot` generation and `gv2gml` for convert `.dot` to readable `.gml` file format. Provides a free viewer [yEd](https://www.yworks.com/products/yed) or [yEd live](https://www.yworks.com/yed-live/?ref=hackernoon.com).

## Usage

Generate graphs only for required library:

- `*_cls.gml` - classes graph (like a UML diagram)
- `*_pkg.gml` - import graph

> **WARNING:** is better to install to a separate environment and use it to analyze your library to exclude external libraries representation in graphs

**Import graph**

Generate import graph from Python library. Works well for namespaces too (packages without `__init__.py` files). **Mark import hierarchy by groups in graph**. Use library folder:

```
import pylibscheme

gml = pylibscheme.create_import_graph('path/to/lib/lib_folder')
```

![alt text](documentation/image-1.png)

**Class graph**

Generate import graph from Python library. Works well for namespaces too (packages without `__init__.py` files). **Mark files witch contain classes by groups in graph**. Use library folder:

```
import pylibscheme

gml = pylibscheme.create_class_graph('path/to/lib/lib_folder')
```

![alt text](documentation/image.png)

## Installation

**Poetry**:

```
poetry install
```

**Conda/mamba**:

```
conda install -f environment.yaml
```

## Plans

- Add CLI usage
- Add more information to graph
- Annotation and another libs support
- Algorithm and performance optimization
