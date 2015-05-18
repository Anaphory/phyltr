from __future__ import division

import math

class CladeProbabilities:

    def __init__(self):

        self.clade_counts = {}
        self.tree_count = 0
        self.caches ={}

    def add_tree(self, tree):

        """Record clade counts for the given tree."""

        cache = tree.get_cached_content()
        self.tree_count += 1
        for subtree in tree.traverse():
            leaves = [leaf.name for leaf in cache[subtree]]
            if len(leaves) == 1:
                continue
            clade = ",".join(sorted(leaves))
            self.clade_counts[clade] = self.clade_counts.get(clade,0) + 1
        self.caches[tree] = cache

    def compute_probabilities(self):

        """Populate the self.clade_probs dictionary with probability values,
        based on the current clade and tree counts."""

        self.clade_probs = {c: self.clade_counts[c] / self.tree_count for c in self.clade_counts}

    def get_tree_prob(self, t):

        """Compute the probability of a tree, as the product of the
        probabilities of all of its constituent clades according to the
        current self.clade_probs values."""

        cache = self.caches.get(t,t.get_cached_content())
        prob = 0
        for node in t.traverse():
            if node == t:
                continue
            leaves = [leaf.name for leaf in cache[node]]
            if len(leaves) == 1:
                continue
            clade = ",".join(sorted(leaves))
            prob += math.log(self.clade_probs[clade])
        return prob

    def annotate_tree(self, tree):

        """Set the support attribute of the nodes in tree using the current
        self.clade_probs values."""

        cache = self.caches.get(tree,tree.get_cached_content())
        for node in tree.traverse():
            leaves = [leaf.name for leaf in cache[node]]
            if len(leaves) == 1:
                continue
            clade = ",".join(sorted(leaves))
            node.support = self.clade_probs[clade]
