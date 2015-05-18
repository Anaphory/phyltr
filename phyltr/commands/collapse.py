"""Usage:
    phyltr collapse [<options>] [<files>]

Collapse monophyletic sets of leaf nodes, by turning their MRCA into a leaf,
and giving the newly formed leaf a specified label.

OPTIONS:

    -t, --translate
        The filename of the translate file.  Each line of the translate file
        should be of the format:
            "label:taxa1,taxa2,taxa3,...."
        The MRCA of the specified taxa will be replaced by a leaf named
        "label".

    files
        A whitespace-separated list of filenames to read treestreams from.
        Use a filename of "-" to read from stdin.  If no filenames are
        specified, the treestream will be read from stdin.
"""

import fileinput

import ete2

import phyltr.utils.phyoptparse as optparse

def read_clade_file(filename):

    """Read a file of names and clade definitions and return a dictionary of
    this data."""

    trans = []
    fp = open(filename, "r")
    for line in fp:
        name, clade = line.strip().split(":")
        clade = clade.strip().split(",")
        trans.append((clade, name))
    fp.close()
    return trans

def run():

    # Parse options
    parser = optparse.OptionParser(__doc__)
    parser.add_option('-t', '--translate',
                help='Specifies the translation file.')
    options, files = parser.parse_args()

    # Read translation file
    try:
        trans = read_clade_file(options.translate)
    except IOError:
        return 1

    # Read trees
    for line in fileinput.input(files):
        t = ete2.Tree(line)
        cache = t.get_cached_content()
        tree_leaves = cache[t]
        for clade, name in trans:
            # Get a list of leaves in this tree
            clade_leaves = [l for l in tree_leaves if l.name in clade]
            if not clade_leaves:
                continue
            # Check monophyly
            mrca = t.get_common_ancestor(clade_leaves)
            mrca_leaves = cache[mrca]
            if set(mrca_leaves) == set(clade_leaves):
                # Clade is monophyletic, so rename and prune
                mrca.name = name
                for child in mrca.get_children():
                    child.detach()

        # Output
        print t.write()

    # Done
    return 0