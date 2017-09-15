import fileinput
import shlex

from phyltr.plumbing.sources import NewickParser
from phyltr.commands.rename import Rename, init_from_args

def test_init_from_args():
    rename, files = init_from_args(shlex.split("--file tests/argfiles/rename.txt"))
    assert rename.remove == False

    rename, files = init_from_args(shlex.split("--file tests/argfiles/rename.txt --remove-missing"))
    assert rename.remove == True

def test_rename():
    lines = fileinput.input("tests/treefiles/basic.trees")
    trees = NewickParser().consume(lines)
    renamed = Rename({"A":"X"}).consume(trees)
    for t in renamed:
        leaves = t.get_leaf_names()
        assert "A" not in leaves
        assert "X" in leaves
        assert all((x in leaves for x in ("B", "C", "D", "E", "F")))

def test_rename_from_file():
    lines = fileinput.input("tests/treefiles/basic.trees")
    trees = NewickParser().consume(lines)
    renamed = Rename(filename="tests/argfiles/rename.txt").consume(trees)
    for t in renamed:
        leaves = t.get_leaf_names()
        assert "A" not in leaves
        assert "X" in leaves
        assert all((x in leaves for x in ("B", "C", "D", "E", "F")))

def test_rename_with_remove():
    lines = fileinput.input("tests/treefiles/basic.trees")
    trees = NewickParser().consume(lines)
    renamed = Rename({
        "A":"U",
        "B":"V",
        "D":"X",
        "E":"Y" }, remove=True).consume(trees)
    for t in renamed:
        leaves = t.get_leaf_names()
        assert all((x in leaves for x in ("U", "V", "X", "Y")))
        assert not any((x in leaves for x in ("A", "B", "C", "D", "E", "F")))

