
from phyltr.commands.base import PhyltrCommand
from phyltr.utils.phyltroptparse import TAXA_FILE_OPTIONS
from phyltr.utils.misc import read_taxa



class Sort(PhyltrCommand):
    """Sort trees according to a desired order of taxa

    If the desired order cannot be achieved, children will be ordered according
    to the median of the desired order of leaves.

    """
    __options__ = TAXA_FILE_OPTIONS + [
        (
            ('taxa',),
            dict(
                metavar='TAXA', nargs='*',
                help="Desired order of taxa")),
    ]

    def __init__(self, **kw):
        PhyltrCommand.__init__(self, **kw)
        if not (self.opts.taxa or self.opts.filename):
            raise ValueError("Must provide a list of taxa or a file containing such a list!")
        if not self.opts.taxa:
            self.opts.taxa = read_taxa(self.opts.filename, column=self.opts.column)
            # FIXME: read_taxa returns a set, we do need an ordered data structure!
        self.opts.taxa = {taxon: t
                          for t, taxon in enumerate(self.opts.taxa)}
        self.median_cache = {}
        if len(self.opts.taxa) == 1:
            raise ValueError("Must specify more than one taxon!")

    def median_desired_leaf_order(self, node):
        leave_indices = frozenset([self.opts.taxa.get(l.name) for l in node.get_leaves()])
        try:
            return self.median_cache[leave_indices]
        except KeyError:
            pass
        leaves = sorted(leave_indices - {None})
        if len(leaves) % 2:
            # Odd number of leaves
            self.median_cache[leave_indices] = leaves[len(leaves) // 2]
        else:
            # Even number of leaves
            self.median_cache[leave_indices] = (leaves[len(leaves) // 2 - 1] + leaves[len(leaves) // 2]) / 2
        return self.median_cache[leave_indices]

    def sort_subtree(self, node):
        children = node.get_children()
        if not children:
            return
        children.sort(key=self.median_desired_leaf_order)
        for descendant in children:
            descendant.detach()
            self.sort_subtree(descendant)
            node.add_child(descendant)

    def process_tree(self, t, _):
        self.sort_subtree(t)
        return t
