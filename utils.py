import os
import time
from enum import StrEnum, IntEnum
from rich import print
from rich.progress import Progress, SpinnerColumn, TextColumn


columns = ['timestamp', 'header_size', 'client_ip',
           'response_code', 'response_size',
           'request_method', 'url', 'username',
           'destination_ip', 'response_type']

FILES = 'files'
FILES_RESULTS = 'files_results'

class LogFields(StrEnum):
    mfip = 'Most Frequent IP'
    lfip = 'Least Frequent IP'
    eps = 'Events per Second'
    bytes = 'Total Bytes'


class FileFormat(StrEnum):
    json = 'json'
    txt = 'txt'
    csv = 'csv'
    log = 'log'


class EXitStatus(IntEnum):
    SUCCESS = 0
    NO_EXIST = 1
    NO_INPUT_FILE_FORMAT = 2
    NO_OUTPUT_FILE_FORMAT = 3
    WRONG_INPUT_FORMAT = 4
    WRONG_OUTPUT_FORMAT = 5
    WRONG_OUTPUT_PATH = 6
    WRONG_INPUT_PATH = 7


ExitCodes = {
    EXitStatus.SUCCESS: 'File(s) exported successfully.',
    EXitStatus.NO_EXIST: 'No such file or directory.',
    EXitStatus.NO_INPUT_FILE_FORMAT: 'Input file does not have a format. '
                                     'Supported formats are: json, txt, csv.',
    EXitStatus.NO_OUTPUT_FILE_FORMAT: 'Output file does not have a format. '
                                      'Supported formats are: json, txt, csv.',
    EXitStatus.WRONG_INPUT_FORMAT: 'Input file does not have correct format. '
                                   'Supported formats are: json, txt, csv.',
    EXitStatus.WRONG_OUTPUT_FORMAT: 'Output file does not have correct format. '
                                   'Supported formats are: json, txt, csv.',
    EXitStatus.WRONG_OUTPUT_PATH: 'Output file does not have the correct path. '
                                    '[HINT] Provide only file name and format. '
                                  'Check README.md on input instructions',
    EXitStatus.WRONG_INPUT_PATH: 'Input file does not have the correct path. '
                                    '[HINT] Check README.md for input instructions.'
}


def generate_file_path(i_input: str, i_output: str) -> [str, str]:
    return os.getcwd() + i_input, os.getcwd() + '/files_results/' + i_output

def handle_error(i_code: EXitStatus, i_path: str, o_path: str) -> str:
    if i_code == EXitStatus.SUCCESS:
        return f'[bold green][SUCCESS][/bold green][italic black]{o_path}[/italic black]: ' \
               f'[green underline]{ExitCodes[i_code]}[/green underline]'
    if i_code in [EXitStatus.NO_EXIST, EXitStatus.NO_INPUT_FILE_FORMAT,
                  EXitStatus.WRONG_INPUT_FORMAT, EXitStatus.WRONG_INPUT_PATH]:
        return f'[bold red][ERROR][/bold red][italic black]{i_path}[/italic black]: ' \
               f'[red underline]{ExitCodes[i_code]}[/red underline]'
    if i_code in [EXitStatus.WRONG_OUTPUT_FORMAT, EXitStatus.NO_OUTPUT_FILE_FORMAT,
                  EXitStatus.WRONG_OUTPUT_PATH]:
        return f'[bold red][ERROR][/bold red][italic black]{o_path}[/italic black]: ' \
               f'[red underline]{ExitCodes[i_code]}[/red underline]'


def get_progress_spinner(i_name: str):
    with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
    ) as progress:
        progress.add_task(description=i_name, total=None)
        time.sleep(0.5)
        print(f'[purple]{i_name}[/purple] ... :magnifying_glass_tilted_right:')

