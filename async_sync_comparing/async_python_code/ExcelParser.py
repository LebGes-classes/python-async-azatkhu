from FileInfo import FileInfo
from pathlib import Path

import numpy as np
import openpyxl as xl
import pandas as pd


class ExcelParser(FileInfo):
    """Парсер Excel."""
    
    __format_of_file = '.xlsx'

    def open_file(self) -> pd.DataFrame:
        """Чтение файла."""

        base_dir = Path(__file__).resolve().parent
        file_path = base_dir.parent / 'excel_data' / (self.get_filename() + self.__format_of_file)
        dataframe = pd.read_excel(file_path)
        
        return dataframe

    def create_file_with_1_sheet(self, data: pd.DataFrame = None, filename: str = '') -> None:
        """Запись DataFrame в Excel файл с 1 листом (страницей).

        Args:
            data: DataFrame, который нужно записать в Excel файл.
            filename: Наименование Excel файла.
        """
        
        data.to_excel(filename, index = False)
        
    def create_file_with_some_sheets(self, dataframes: list = [pd.DataFrame], filenames: list = [str], index: int = 0) -> None:
        """Запись нескольких DataFrame в Excel файл с несколькими листами (страницами).

        Args:
            dataframes: Список с несколькими DataFrame.
            filenames: Список с наименованиями страниц для соответствующих DataFrame в создаваемом Excel файле.
        """

        base_dir = Path(__file__).resolve().parent
        with pd.ExcelWriter(f'{base_dir.parent}/async_result_xlsx/RESULT_OF_ANALYSING_{index}.xlsx') as writer:
            for dataframe, filename in zip(dataframes, filenames):
                dataframe.to_excel(writer, sheet_name = filename, index = False)
