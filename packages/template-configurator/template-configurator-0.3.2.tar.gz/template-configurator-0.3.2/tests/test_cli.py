import argparse
import filecmp
import os
import re
import shutil
import unittest
from contextlib import redirect_stdout, redirect_stderr
from filecmp import dircmp
from io import StringIO
from typing import Optional, Set

from hbreader import hbread

from template_configurator import configure


class ArgParseExitException(Exception):
    ...


def _parser_exit(_: argparse.ArgumentParser,  __=0, message: Optional[str]=None) -> None:
    raise ArgParseExitException(message)


argparse.ArgumentParser.exit = _parser_exit

expected_file_output = """actual/mkdocs.yml written
actual/requirements.txt written
actual/Makefile written
actual/README.md written
actual/Pipfile written
actual/setup.py written
actual/.gitignore written
actual/tox.ini written
actual/setup.cfg written
actual/make-venv/README.md written
actual/make-venv/Pipfile written
actual/tests/test_input_against_model.py written
actual/tests/__init__.py written
actual/tests/input/CONFIG.yaml written
actual/tests/input/README.md written
actual/.github/workflows/pypi-publish.yaml written
actual/.github/workflows/main.yaml written
actual/model/docs/credits.md written
actual/model/docs/home.md written
actual/model/schema/sample_model.yaml written
"""

expected_file_output_2 = """actual/mkdocs.yml skipped - copy already exists
actual/requirements.txt skipped - copy already exists
actual/Makefile skipped - copy already exists
actual/README.md skipped - copy already exists
actual/Pipfile skipped - copy already exists
actual/setup.py skipped - copy already exists
actual/.gitignore skipped - copy already exists
actual/tox.ini skipped - copy already exists
actual/setup.cfg skipped - copy already exists
actual/make-venv/README.md skipped - copy already exists
actual/make-venv/Pipfile skipped - copy already exists
actual/tests/test_input_against_model.py skipped - copy already exists
actual/tests/__init__.py skipped - copy already exists
actual/tests/input/CONFIG.yaml skipped - copy already exists
actual/tests/input/README.md skipped - copy already exists
actual/.github/workflows/pypi-publish.yaml skipped - copy already exists
actual/.github/workflows/main.yaml skipped - copy already exists
actual/model/docs/credits.md skipped - copy already exists
actual/model/docs/home.md skipped - copy already exists
actual/model/schema/sample_model.yaml skipped - copy already exists
"""


class TestCLI(unittest.TestCase):
    cwd = os.path.dirname(__file__)
    expected_dir = os.path.join(cwd, 'expected')
    expected_target_dir = os.path.join(expected_dir, 'output')
    actual_dir = os.path.join(cwd, 'actual')
    help_fname = os.path.join(expected_dir, 'help')
    config_file = os.path.join(cwd, 'test_config/CONFIG.yaml')
    test_template_dir = os.path.join(cwd, 'input/templates')

    @classmethod
    def setUpClass(cls) -> None:
        if os.path.exists(cls.actual_dir):
            shutil.rmtree(cls.actual_dir)
        os.makedirs(cls.actual_dir, exist_ok=True)

    @unittest.skipIf(os.environ.get('IN_TOX', False), "Disabled to to tox line folding at 60 characters")
    def test_help(self):
        """ Make sure the help output works """
        self.maxDiff = None
        outf = StringIO()
        with redirect_stdout(outf):
            try:
                print(configure.main(["-h"]))
            except ArgParseExitException:
                pass
        if os.path.exists(self.help_fname):
            expected = hbread(self.help_fname)
            # Note: Tox fails this test because it uses a 60 character output wrap
            self.assertEqual(expected, outf.getvalue())
        else:
            with open(self.help_fname, 'w') as f:
                f.write(outf.getvalue())
            self.fail("Help text written to test file.  Run again...")

    def test_bad_config_file(self):
        """ Make sure we detect a bad configuration file """
        outf = StringIO()
        with redirect_stderr(outf):
            with self.assertRaises(ArgParseExitException) as e:
                configure.main([self.config_file + 'z'])
            self.assertIn("can't open ", str(e.exception))

    def test_bad_template_dir(self):
        """ Make sure we detect a bad template directory """
        outf = StringIO()
        with redirect_stderr(outf):
            with self.assertRaises(NotADirectoryError) as e:
                configure.main([self.config_file,
                                "--templatedir", os.path.join(self.expected_dir, 'nodir')])
            self.assertIn("/nodir does not exist", str(e.exception))

    def test_bad_target_directory(self):
        """ Make sure we detect a bad target directory """
        outf = StringIO()
        with redirect_stderr(outf):
            with self.assertRaises(NotADirectoryError) as e:
                configure.main([self.config_file,
                                "-t", os.path.join(self.expected_dir, 'nodir')])
            self.assertIn("/nodir does not exist", str(e.exception))

    def test_simple_conversion(self):
        """ Run the conversion against a fixed set of test_templates """

        def are_dir_trees_equal(dir1, dir2):
            """
            Compare two directories recursively. Files in each directory are
            assumed to be equal if their names and contents are equal.

            @param dir1: First directory path
            @param dir2: Second directory path

            @return: True if the directory trees are the same and
                there were no errors while accessing the directories or files,
                False otherwise.
           """
            dirs_cmp = filecmp.dircmp(dir1, dir2)
            if len(dirs_cmp.left_only) > 0 or len(dirs_cmp.right_only) > 0 or \
                    len(dirs_cmp.funny_files) > 0:
                return False
            (_, mismatch, errors) = filecmp.cmpfiles(
                dir1, dir2, dirs_cmp.common_files, shallow=False)
            if len(mismatch) > 0 or len(errors) > 0:
                return False
            for common_dir in dirs_cmp.common_dirs:
                new_dir1 = os.path.join(dir1, common_dir)
                new_dir2 = os.path.join(dir2, common_dir)
                if not are_dir_trees_equal(new_dir1, new_dir2):
                    return False
            return True

        def tweak_output(output: str) -> Set[str]:
            """ Fix relative path issues """
            return as_set(re.sub(r'.*/actual/', 'actual/', output))

        def as_set(txt: str) -> Set[str]:
            return set(txt.split('\n'))

        self.maxDiff = None
        outf = StringIO()
        with redirect_stdout(outf):
            configure.main(['-t', self.actual_dir,
                            '--templatedir', self.test_template_dir,
                            self.config_file])
        self.assertEqual(as_set(expected_file_output), tweak_output(outf.getvalue()))

        outf = StringIO()
        with redirect_stdout(outf):
            configure.main(['-t', self.actual_dir,
                            '--templatedir', self.test_template_dir,
                            self.config_file])
        self.assertEqual(as_set(expected_file_output_2), tweak_output(outf.getvalue()))

        outf = StringIO()
        with redirect_stdout(outf):
            configure.main(['-t', self.actual_dir, '--reset',
                            '--templatedir', self.test_template_dir,
                            self.config_file])
        self.assertEqual(as_set(expected_file_output), tweak_output(outf.getvalue()))

        if not are_dir_trees_equal(self.expected_target_dir, self.actual_dir):
            dcmp = dircmp(self.expected_target_dir,
                          '--templatedir', self.test_template_dir,
                          self.actual_dir)
            print(dcmp.report())
            self.fail("Expected output doesn't match actual")


if __name__ == '__main__':
    unittest.main()
