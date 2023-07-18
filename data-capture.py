import pandas as pd

class DataCapture:
    """
    This class is used to capture data from a given URL and sheet name.
    It can return a dataframe of the data and clean columns from the dataframe if specified.

    Args:
        url (str): The URL of the Google Sheets document.
        sheet_name (str or list of str, optional): The name of the sheet(s) to capture data from.
            If a list is provided, multiple datasets will be concatenated.
            If not specified, the first sheet will be used.
        date_parse (bool or list of bool, optional): If True or a list of True values, the specified date columns
            will be parsed as dates when reading the CSV data.
            If not specified, dates will not be parsed.
        with_del_columns (str or list of str, optional): The column name(s) to delete from the resulting dataframe.
            If a list is provided, multiple columns will be dropped.
            If not specified, no columns will be deleted.

    Attributes:
        url (str): The URL of the Google Sheets document.
        sheet_name (str or list of str): The name of the sheet(s) to capture data from.
        date_parse (bool or list of bool): Whether to parse date columns as dates or not.
        with_del_columns (str or list of str): The column name(s) to delete from the resulting dataframe.
        dataframe (pandas.DataFrame): The captured data as a pandas DataFrame.

    Methods:
        capture(): Captures the data from the specified URL and sheet name(s) and returns the resulting dataframe.
        _single_dataset(): Captures data from a single dataset (sheet) and returns the resulting dataframe.
        _multiple_datasets(): Captures data from multiple datasets (sheets) and concatenates them into a single dataframe.
        _clean_columns(): Deletes specified columns from the dataframe.
        _format_sheet_name(sheet_name): Formats the sheet name to be used in the URL.

    Examples:
        # Capture data from a single sheet
        capture_single = DataCapture(url='your_url', sheet_name='Sheet1')
        dataframe_single = capture_single.capture()

        # Capture data from multiple sheets and clean columns
        capture_multiple = DataCapture(url='your_url', sheet_name=['Sheet1', 'Sheet2'], with_del_columns=['Column1', 'Column2'])
        dataframe_multiple = capture_multiple.capture()
    """
    def __init__(self, url, sheet_name=None, date_parse=None, with_del_columns=None):
        self.url = url
        self.sheet_name = sheet_name
        self.date_parse = date_parse
        self.with_del_columns = with_del_columns
        self.dataframe = None

    def capture(self):
        """
        Captures the data from the specified URL and sheet name(s) and returns the resulting dataframe.

        Returns:
            pandas.DataFrame: The captured data as a pandas DataFrame.
        """
        if isinstance(self.sheet_name, list):
            self.dataframe = self._multiple_datasets()
        else:
            self.dataframe = self._single_dataset()

        if isinstance(self.with_del_columns, list):
            self._clean_columns()

        return self

    def _single_dataset(self):
        """
        Captures data from a single dataset (sheet) and returns the resulting dataframe.

        Returns:
            pandas.DataFrame: The captured data as a pandas DataFrame.
        """
        sheet = self._format_sheet_name(self.sheet_name)
        url = f"https://docs.google.com/spreadsheets/d/{self.url.split('/')[5]}/gviz/tq?tqx=out:csv&sheet={sheet}"
        if self.date_parse:
            return pd.read_csv(url, header='infer', parse_dates=self.date_parse)
        else:
            return pd.read_csv(url, header='infer')

    def _multiple_datasets(self):
        """
        Captures data from multiple datasets (sheets) and concatenates them into a single dataframe.

        Returns:
            pandas.DataFrame: The concatenated dataframe containing data from all the specified sheets.
        """
        result = pd.DataFrame()
        for sheet in self.sheet_name:
            sheet = self._format_sheet_name(sheet)
            url = f"https://docs.google.com/spreadsheets/d/{self.url.split('/')[5]}/gviz/tq?tqx=out:csv&sheet={sheet}"
            temp_dataframe = pd.read_csv(url, header='infer')
            temp_dataframe["spreadsheet_tab"] = sheet
            result = pd.concat([result, temp_dataframe])
        return result

    def _clean_columns(self):
        """
        Deletes specified columns from the dataframe.

        Returns:
            None
        """
        if isinstance(self.with_del_columns, list):
            for column in self.with_del_columns:
                self.dataframe = self.dataframe.drop(column, axis=1)
        else:
            self.dataframe = self.dataframe.drop(self.with_del_columns, axis=1)

    @staticmethod
    def _format_sheet_name(sheet_name):
        """
        Formats the sheet name to be used in the URL.

        Args:
            sheet_name (str): The name of the sheet.

        Returns:
            str: The formatted sheet name.
        """
        sheet = sheet_name.replace(' ', '%20')
        sheet = sheet.replace('&', '%26')
        return sheet