import pytest

from phyltr import build_pipeline
from phyltr.commands.sibling import Sibling

def test_init_from_args():
    Sibling.init_from_args("A")

def test_bad_init_no_args():
    with pytest.raises(SystemExit):
        Sibling.init_from_args('')

def test_sibling(basictrees):
    siblings = list(Sibling(taxon="A").consume(basictrees))
    assert siblings == ["B","C","B","B","C","B"]

def test_non_leaf_sibling(basictrees):
    siblings = list(build_pipeline("sibling C", source=basictrees))
    assert siblings == ["(A,B)","A","(A,B)","(A,B)","A","E"]

def test_bad_params_missing_taxa(basictrees):
    with pytest.raises(ValueError):
        list(Sibling(taxon="X").consume(basictrees))
