# Copyright (C) 2021 Andrea Francia Bereguardo(PV) Italy
from textwrap import dedent

import pytest

from tests import run_command
from tests.run_command import first_line_of
from tests.run_command import last_line_of
from tests.run_command import temp_dir  # noqa
from tests.support.my_path import MyPath
from trashcli.lib.exit_codes import EX_IOERR


@pytest.mark.slow
class TestEndToEndPut:
    def setup_method(self):
        self.tmp_dir = MyPath.make_temp_dir()

    def test_last_line_of_help(self, temp_dir):
        result = run_command.run_command(temp_dir, "trash-put", ['--help'])

        assert last_line_of(result.stdout) == \
               'Report bugs to https://github.com/andreafrancia/trash-cli/issues'

    def test_without_args(self, temp_dir):
        result = run_command.run_command(temp_dir, "trash-put", [])

        assert [first_line_of(result.stderr),
                result.exit_code] == \
               ['usage: trash-put [OPTION]... FILE...', 2]

    def test_wrong_option(self, temp_dir):
        result = run_command.run_command(temp_dir, "trash-put", ['--wrong-option'])

        assert [last_line_of(result.stderr),
                result.exit_code] == \
               ['trash-put: error: unrecognized arguments: --wrong-option', 2]

    def test_on_help(self, temp_dir):
        result = run_command.run_command(temp_dir, "trash-put", ['--help'])

        assert [result.reformatted_help(),
                result.exit_code] == \
               [dedent('''\
                usage: trash-put [OPTION]... FILE...

                Put files in trash

                positional arguments:
                  files

                options:
                  -h, --help            show this help message and exit
                  --print-completion {bash,zsh,tcsh}
                                        print shell completion script
                  -d, --directory       ignored (for GNU rm compatibility)
                  -f, --force           silently ignore nonexistent files
                  -i, --interactive     prompt before every removal
                  -r, -R, --recursive   ignored (for GNU rm compatibility)
                  --trash-dir TRASHDIR  use TRASHDIR as trash folder
                  -v, --verbose         explain what is being done
                  --version             show program's version number and exit

                To remove a file whose name starts with a '-', for example '-foo',
                use one of these commands:

                    trash -- -foo

                    trash ./-foo

                Report bugs to https://github.com/andreafrancia/trash-cli/issues
            '''), 0]

    def test_it_should_skip_dot_entry(self, temp_dir):
        result = run_command.run_command(temp_dir, "trash-put", ['.'])

        assert [result.stderr, result.exit_code] == \
               ["trash-put: cannot trash directory '.'\n", EX_IOERR]

    def test_it_should_skip_dotdot_entry(self, temp_dir):
        result = run_command.run_command(temp_dir, "trash-put", ['..'])

        assert [result.stderr, result.exit_code] == \
               ["trash-put: cannot trash directory '..'\n", EX_IOERR]

    def test_it_should_print_usage_on_no_argument(self, temp_dir):
        result = run_command.run_command(temp_dir, "trash-put", [])

        assert [result.stdout, result.stderr, result.exit_code] == \
               ['', 'usage: trash-put [OPTION]... FILE...\n'
                'trash-put: error: Please specify the files to trash.\n', 2]

    def test_it_should_skip_missing_files(self, temp_dir):
        result = run_command.run_command(temp_dir, "trash-put",
                                         ['-f', 'this_file_does_not_exist', 'nor_does_this_file'])

        assert [result.stdout, result.stderr, result.exit_code] == ['', '', 0]

