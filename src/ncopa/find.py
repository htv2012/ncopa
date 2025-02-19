def find_all(directive, predicate):
    """Search a directive using a predicate."""
    found = (node for node in directive if predicate(node))
    return found


def find_next(directive, predicate):
    found = next(find_all(directive, predicate))
    return found


# A few predicates
def by_name(name):
    """Search by name."""

    def match(directive):
        """Return True if a directive name matched."""
        return directive.name == name

    return match


def by_any_args(args):
    def match(directive):
        return set(args).issubset(directive.args)

    return match


def all_of(*predicates):
    def match(directive):
        return all(predicate(directive) for predicate in predicates)

    return match


def any_of(*predicates):
    def match(directive):
        return any(predicate(directive) for predicate in predicates)

    return match


def negative(predicate):
    def match(directive):
        return not predicate(directive)

    return match
