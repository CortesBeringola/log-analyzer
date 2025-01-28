import os, glob
import typer
from rich import print
from LogFile import InputLogFile, OutputLogFile
from typing import Optional
from utils import EXitStatus, generate_file_path, handle_error, get_progress_spinner, FILES

app = typer.Typer()

@app.command(help='IMPORTANT INFORMATION: Please check the README.md file for detailed instructions.')
def main(i_path: str, o_path: str, i_mfip: Optional[bool] = False,
         i_lfip: Optional[bool] = False, i_eps:  Optional[bool] = False,
         i_bytes:  Optional[bool] = False):

    input_path, output_path = generate_file_path(i_path, o_path)
    output_file = OutputLogFile(output_path)
    try:
        if os.path.isdir(input_path):  # path corresponds to directory
            f_format = i_path.split('/')[-2] if i_path[-1] == '/' else i_path.split('/')[-1]
            if f_format == FILES:
                output_file.file_code = EXitStatus.WRONG_INPUT_PATH
                raise typer.Exit()
            for file in glob.glob(os.path.join(input_path, f'*.{f_format}')):
                logs = InputLogFile(file)
                get_progress_spinner(logs.file_name)
                if logs.file_code == EXitStatus.WRONG_INPUT_FORMAT:
                    output_file.file_code = logs.file_code
                    raise typer.Exit()
                output_file.output_data = output_file.output_data | logs.analyze_data(i_mfip, i_lfip, i_eps, i_bytes)
        elif os.path.isfile(input_path):  # path corresponds to file
            logs = InputLogFile(input_path)
            get_progress_spinner(logs.file_name)
            if logs.file_code == EXitStatus.WRONG_INPUT_FORMAT:
                output_file.file_code = logs.file_code
                raise typer.Exit()
            output_file.output_data = logs.analyze_data(i_mfip, i_lfip, i_eps, i_bytes)
        else:  # The inputted path does not exist
            output_file.file_code = EXitStatus.NO_EXIST
            raise typer.Exit()

        # Export result if selected format is json, txt or csv
        output_file.export_result()

        raise typer.Exit()

    except Exception:
        msg = handle_error(output_file.file_code, input_path, output_path)
        print(msg)


if __name__ == "__main__":
    app()
