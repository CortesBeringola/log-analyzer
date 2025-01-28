import os
from typer.testing import CliRunner
from utils import ExitCodes, EXitStatus
from cli import app

runner = CliRunner()


def test_incomplete_parameters():  # Raises error
    result = runner.invoke(app, ['access_copy.log'])
    assert result.exit_code == 2


def test_path_does_not_exist():  # Incorrect path raises error
    result = runner.invoke(app, ['/files/wrong_file.log', 'test.json'])
    file_path = os.getcwd() + '/files/wrong_file.l\nog'
    error_msg = f'[ERROR]{file_path}: {ExitCodes[EXitStatus.NO_EXIST]}'
    assert error_msg in result.stdout


def test_incorrect_input_format():  # Test incorrect input format
    result = runner.invoke(app, ['/files/log/short_file.xml', 'test.csv'])
    file_path = os.getcwd() + '/files/log/short_fi\nle.xml'
    error_msg = f'[ERROR]{file_path}: Input file does not have correct format. Supported' \
                ' formats are: json, \ntxt, csv.'
    assert error_msg in result.stdout


def test_no_output_format():  # Test output file with no format
    result = runner.invoke(app, ['/files/log/short_file.log', 'test'])
    file_path = os.getcwd() + '/files_results/test\n'
    error_msg = f'[ERROR]{file_path}: {ExitCodes[EXitStatus.NO_OUTPUT_FILE_FORMAT]}'
    assert error_msg in result.stdout


def test_incorrect_output_format():  # Test output file with wrong format
    result = runner.invoke(app, ['/files/log/short_file.log', 'test.xml'])
    file_path = os.getcwd() + '/files_results/test\n.xml'
    error_msg = f'[ERROR]{file_path}: Output file does not have correct ' \
                f'format. Supported formats are: json, \ntxt, csv.'

    assert error_msg in result.stdout
