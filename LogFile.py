import json
from typing import Optional

import pandas as pd
from utils import columns, FileFormat, EXitStatus, LogFields, FILES_RESULTS

class LogFile:
    def __init__(self, i_file_path: str):
        self.file_code = None
        self.ip_df = None
        self.output_data = {}
        self.file_path = i_file_path
        self.file_name = i_file_path.split('/')[-1]
        self.file_format = self._get_format()

    def _get_format(self) -> EXitStatus | str | None:
        return None


class InputLogFile(LogFile):
    def __init__(self, i_path_name):
        super().__init__(i_path_name)
        self.input_data = self.parse_file()

    def _get_format(self) -> str | None:
        if '.' not in self.file_path:
            self.file_code = EXitStatus.NO_INPUT_FILE_FORMAT
        return None if '.' not in self.file_path else self.file_path.split('.')[1]

    def _get_ip_frequency(self):
        self.ip_df = self.input_data.groupby(['client_ip'])['client_ip']\
            .count()\
            .reset_index(name='count')\
            .sort_values(['count'], ascending=False)

    def _get_most_frequent_ip(self):
        if not isinstance(self.ip_df, pd.DataFrame):
            self._get_ip_frequency()
        return self.ip_df.head(1).to_dict('records')[0]

    def _get_least_frequent_ip(self):
        if not isinstance(self.ip_df, pd.DataFrame):
            self._get_ip_frequency()
        return self.ip_df.tail(1).to_dict('records')[0]

    def _get_events_per_second(self):
        if len(self.input_data) > 1:
            max_value = float(self.input_data['timestamp'].max())
            min_value = float(self.input_data['timestamp'].min())
            return len(self.input_data['timestamp'])/(max_value-min_value)
        else:
            return 'Not enough logs in this file to calculate its EPS ' \
                   '(Events per second)'

    def _get_total_bytes(self):
        self.input_data['response_size'] = self.input_data['response_size'].astype(float)
        return float(self.input_data['response_size'].sum())

    def analyze_data(self, i_mfip: Optional[bool] = False, i_lfip: Optional[bool] = False,
                   i_eps: Optional[bool] = False, i_bytes: Optional[bool] = False):
        if isinstance(self.input_data, pd.DataFrame) and not self.input_data.empty:
            if i_mfip:
                self.output_data[LogFields.mfip.value] = self._get_most_frequent_ip()
            if i_lfip:
                self.output_data[LogFields.lfip.value] = self._get_least_frequent_ip()
            if i_eps:
                self.output_data[LogFields.eps.value] = self._get_events_per_second()
            if i_bytes:
                self.output_data[LogFields.bytes.value] = self._get_total_bytes()

            if not any([i_mfip, i_lfip, i_eps, i_bytes]):  # no arguments means pass all fields
                self.output_data = {
                    LogFields.mfip.value: self._get_most_frequent_ip(),
                    LogFields.lfip.value: self._get_least_frequent_ip(),
                    LogFields.eps.value: self._get_events_per_second(),
                    LogFields.bytes.value: self._get_total_bytes()
                }
        else:
            self.output_data = {self.file_name: 'Empty log file'}
        return {self.file_name: self.output_data}


    @staticmethod
    def parse_file_lines(i_line: list[str]):
        df_data = []
        for line in i_line:  # Parse line to clean data
            line = line.replace('\n', '')
            line_split = [x for x in line.split(' ') if x.strip()]
            df_data.append(dict(zip(columns, line_split)))
        return df_data

    def parse_file(self) -> pd.DataFrame:
        if self.file_format == FileFormat.csv:  # Parse CSV file
            return pd.read_csv(self.file_path, header=None, names=columns)
        elif self.file_format in [FileFormat.txt, FileFormat.log, FileFormat.json]:
            with open(self.file_path) as file:
                if self.file_format == FileFormat.json:  # Parse JSON file
                    data = json.load(file)
                    return pd.DataFrame.from_dict(data, orient='index')
                else:
                    file = file.readlines()  # Parse txt or log file
                    data = self.parse_file_lines(file)
                return pd.DataFrame(data)
        elif not self.file_format:
            self.file_code = EXitStatus.NO_INPUT_FILE_FORMAT
        else:
            self.file_code = EXitStatus.WRONG_INPUT_FORMAT.value





class OutputLogFile(LogFile):

    def _get_format(self) -> str | None:
        return None if '.' not in self.file_path else self.file_path.split('.')[1]

    def export_result(self):
        if self.file_path.split('/')[-2] != FILES_RESULTS:
            self.file_code = EXitStatus.WRONG_OUTPUT_PATH
            return
        if self.file_format == FileFormat.json:
            with open(self.file_path, 'w') as f:
                json.dump(self.output_data, f)
            self.file_code = EXitStatus.SUCCESS
        elif self.file_format == FileFormat.txt:
            with open(self.file_path, 'w') as f:
                for key, value in self.output_data.items():
                    f.write(str(key) + ' >>> ' + str(value) + '\n')
            self.file_code = EXitStatus.SUCCESS
        elif self.file_format == FileFormat.csv:
            df = pd.DataFrame.from_dict(data=self.output_data, orient="index")
            df.to_csv(self.file_path)
            self.file_code = EXitStatus.SUCCESS
        elif not self.file_format:
            self.file_code = EXitStatus.NO_OUTPUT_FILE_FORMAT
        else:
            self.file_code = EXitStatus.WRONG_OUTPUT_FORMAT

