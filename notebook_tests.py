import fnmatch
import os
import subprocess
import tempfile

import nbformat


def _notebook_run(path):
    """
        Execute a notebook via nbconvert and collect output.
       :returns (parsed nb object, execution errors)
    """
    dirname, __ = os.path.split(path)
    os.chdir(dirname)
    with tempfile.NamedTemporaryFile(suffix=".ipynb") as fout:
        args = [
            "jupyter", "nbconvert", "--to", "notebook", "--execute",
            "--ExecutePreprocessor.timeout=60",
            "--output", fout.name, path]
        subprocess.check_call(args)

        fout.seek(0)
        nb = nbformat.read(fout, nbformat.current_nbformat)

    errors = [
        output for cell in nb.cells if "outputs" in cell
        for output in cell["outputs"] if output.output_type == "error"]

    return nb, errors


def test_ipynb():
    src = os.getcwd()
    for root, dirnames, filenames in os.walk(src):
        for filename in fnmatch.filter(filenames, '*.ipynb'):
            path = os.path.join(src, filename)
            print("Detected ipython notebook {} to run tests on".format(path))
            nb, errors = _notebook_run(path)
            assert errors == []
