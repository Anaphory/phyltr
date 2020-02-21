from phyltr.commands.base import PhyltrCommand
from phyltr.utils.phyltroptparse import TAXA_FILE_OPTIONS
from phyltr.utils.misc import read_taxa

def find_polytomy(t):
    for s in t.traverse():
        if not s.is_leaf() or len(s.descendants) == 2:
            return s


class Problematic(PhyltrCommand):
    """
    Filter trees according to whether they have certain issues for other tools
    """
    __options__ = [
        (
            ('-b', '--binary', '--without-polytomies'),
            dict(
                action="store_true", default=None, dest="binary",
                help='Only return binary trees')),
        (
            ('-B', '--non-binary', '--with-polytomies'),
            dict(
                action="store_false", default=None, dest="binary",
                help='Only return trees that are non-binary somewhere')),
    ]

    def __init__(self, **kw):
        PhyltrCommand.__init__(self, **kw)
        ...

    def process_tree(self, t, _):
        if self.opts.binary is None:
            pass
        else:
            is_binary = find_polytomy(t)
            if (self.opts.binary and is_binary) or (not self.opts.binary and not is_binary):
                return t
            else:
                return
