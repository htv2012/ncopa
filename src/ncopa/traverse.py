import collections

from ncopa import Directive


def depth_first_traversal(directive: Directive, visit, parents: tuple = None):
    """Depth-first traverse."""
    parents = parents or tuple()
    visit(directive, parents)
    for node in directive:
        depth_first_traversal(node, visit, parents=parents + (directive,))


def breadth_first_traversal(directive: Directive, visit, parents: tuple = None):
    """Breadth-first traverse."""
    parents = parents or tuple()
    stack = collections.deque([(directive, parents)])
    while stack:
        directive, parents = stack.popleft()
        visit(directive, parents)
        for sub_directive in directive:
            stack.append((sub_directive, parents + (directive,)))
