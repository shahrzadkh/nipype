# -*- coding: utf-8 -*-
# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:
from __future__ import print_function, unicode_literals
import os
import pytest

from nipype.interfaces import utility
import nipype.pipeline.engine as pe


def test_rename(tmpdir):
    os.chdir(str(tmpdir))

    # Test very simple rename
    _ = open("file.txt", "w").close()
    rn = utility.Rename(in_file="file.txt", format_string="test_file1.txt")
    res = rn.run()
    outfile = str(tmpdir.join("test_file1.txt"))
    assert res.outputs.out_file == outfile
    assert os.path.exists(outfile)

    # Now a string-formatting version
    rn = utility.Rename(in_file="file.txt", format_string="%(field1)s_file%(field2)d", keep_ext=True)
    # Test .input field creation
    assert hasattr(rn.inputs, "field1")
    assert hasattr(rn.inputs, "field2")

    # Set the inputs
    rn.inputs.field1 = "test"
    rn.inputs.field2 = 2
    res = rn.run()
    outfile = str(tmpdir.join("test_file2.txt"))
    assert res.outputs.out_file == outfile
    assert os.path.exists(outfile)


@pytest.mark.parametrize("args, expected", [
        ({}                ,  ([0], [1,2,3])),
        ({"squeeze" : True},  (0  , [1,2,3]))
        ])
def test_split(tmpdir, args, expected):
    os.chdir(str(tmpdir))

    node = pe.Node(utility.Split(inlist=list(range(4)),
                                 splits=[1, 3],
                                 **args),
                   name='split_squeeze')
    res = node.run()
    assert res.outputs.out1 == expected[0]
    assert res.outputs.out2 == expected[1]
