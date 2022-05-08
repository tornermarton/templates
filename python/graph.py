# coding=utf-8
__all__ = [
    "Vertex",
    "DirectedEdge",
    "DirectedGraph"
]

from dataclasses import dataclass
from typing import Optional, TypeVar, Generic

T = TypeVar('T')


@dataclass(frozen=True, eq=True)
class Vertex(Generic[T]):
    name: str
    value: Optional[T] = None


@dataclass(frozen=True, eq=True)
class DirectedEdge(object):
    head: str
    tail: str


@dataclass
class DirectedGraph(object):
    vertices: set[Vertex]
    edges: set[DirectedEdge]

    def _is_valid_edge(self, e: DirectedEdge) -> bool:
        return (
            self._graph_dict.get(e.tail, None) is not None and
            self._graph_dict.get(e.head, None) is not None
        )

    def __init__(
        self,
        vertices: Optional[set[Vertex]] = None,
        edges: Optional[set[DirectedEdge]] = None,
    ) -> None:
        self._vertices: set[Vertex] = set()
        self._edges: set[DirectedEdge] = set()

        self._graph_dict: dict[str, set[str]] = {}

        if vertices:
            for v in vertices:
                self.add_vertex(v)

        if edges:
            for e in edges:
                self.add_edge(e)

    @property
    def vertices(self) -> set[Vertex]:
        return self._vertices

    @property
    def edges(self) -> set[DirectedEdge]:
        return self._edges

    @property
    def graph_dict(self) -> dict[str, set[str]]:
        return self._graph_dict

    def add_vertex(self, v: Vertex) -> None:
        if self._graph_dict.get(v.name, None) is not None:
            raise ValueError(f"This graph already has a vertex named {v.name}")

        self._vertices.add(v)
        self._graph_dict[v.name] = set()

    def add_edge(self, e: DirectedEdge) -> None:
        if not self._is_valid_edge(e):
            raise ValueError(
                f"The endpoint(s) of the edge {e} cannot be found in the graph."
            )

        self._edges.add(e)
        self._graph_dict[e.tail].add(e.head)

    def _has_circle_until(
        self,
        vertex: str,
        visited_global: dict[str, bool],
        visited_recursion: dict[str, bool],
    ) -> bool:
        visited_global[vertex] = True
        visited_recursion[vertex] = True

        for neighbor in self._graph_dict[vertex]:
            if (
                visited_recursion[neighbor] or
                not visited_global[neighbor] and
                self._has_circle_until(
                    neighbor,
                    visited_global,
                    visited_recursion
                )
            ):
                return True

        visited_recursion[vertex] = False

        return False

    def has_circle(self) -> bool:
        vertex_names: list[str] = list(self._graph_dict.keys())

        visited_global: dict[str, bool] = {v: False for v in vertex_names}
        visited_recursion: dict[str, bool] = {v: False for v in vertex_names}

        for vertex in vertex_names:
            if not visited_global[vertex]:
                if self._has_circle_until(
                    vertex=vertex,
                    visited_global=visited_global,
                    visited_recursion=visited_recursion,
                ):
                    return True

        return False


if __name__ == '__main__':
    g = DirectedGraph(
        vertices={Vertex("a"), Vertex("b")},
        edges={DirectedEdge("a", "b")}
    )
    g.add_vertex(Vertex("c"))
    g.add_edge(DirectedEdge("b", "c"))

    print(g.has_circle())

    g.add_edge(DirectedEdge("c", "a"))

    print(g.has_circle())

    g.add_edge(DirectedEdge("c", "d"))
