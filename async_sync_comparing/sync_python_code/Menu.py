from AnalyzeMedicalDiagnosticDevices import AnalyzeMedicalDiagnosticDevices
from ExcelParser import ExcelParser


class Menu:
    """Класс Меню."""
    
    def __init__(self) -> None:
        """Конструктор класса."""
        
        self.__files = [f'medical_diagnostic_devices_{i}' for i in range(1, 11)]
        self.__analysing_devices = [AnalyzeMedicalDiagnosticDevices(file) for file in self.__files]
        self.__count = 0
        self.__results = []
    
    def choose_filter_warranty_option(self) -> None:
        """Вывод вариантов для выбора типа фильтрации даты последней гарантии медицинских устройств."""
        
        print('Как нужно отфильтровать дату гарантии?')
        print('1 - гарантия не истекла.')
        print('2 - гарантия истекла.')
        print('3 - сегодня последний гарантийный день.')
        print('4 - сортировка гарантии по возрастанию.')
        print('5 - сортировка гарантии по убыванию.')
        
    def choose_calibration_time(self) -> None:
        """Вывод вариантов для выбора временного отрезка последней калибровки медицинского устройства."""
        
        print('Какие даты калибровки хотите увидеть?')
        print('1 - дата калибровки еще не настала.')
        print('2 - дата последней калибровки была в прошлом.')
        print('3 - дата калибровки ошибочная (до даты установки оборудования).')
    
    def process_of_analysing(
        self, 
        analyzer: AnalyzeMedicalDiagnosticDevices = None, 
        choice_warranty_until_filter: int = 1, 
        choose_last_calibration_time: int = 1, 
        count_of_clinics: int = 1
    ) -> None:
        """Процесс анализа, включающий все функции класса анализа медицинских устройств.
        
        Args:
            analyzer: экзепляр класса AnalyzeMedicalDiagnosticDevices.
            choice_warranty_until_filter: пользовательский ввод для выбора типа фильтрации даты последней гарантии мед устройств.
            choose_last_calibration_time: пользовательский ввод для выбора временного отрезка последней калибровки медицинского устройства.
            count_of_clinics: пользовательский ввод для выбора количества клиник, для которых нужно увидеть количество проблем.
        """
        
        self.__count += 1
        analyzer.get_dataframe_from_file()

        print(self.__count, 'файл прочитан.')
        
        analyzer.filter_out_date('warranty_until')
        analyzer.filter_out_date('install_date')
        analyzer.filter_out_date('last_calibration_date')
        analyzer.filter_out_date('last_service_date')   

        print('Даты приведены к одному виду.')
        
        analyzer.normalize_status_of_device()

        print('Нормализованы статусы устройств.')
        
        df1 = analyzer.filtering_warranty_dates(choice_warranty_until_filter)

        print('Даты окончания гарантии отфильтрованы, создан файл xlsx.')
        
        analyzer.sort_issues_reported()

        print('Отсортированы проблемы устройств по клиникам.')

        df2 = analyzer.show_clinics_with_problems(count_of_clinics)

        print('Создан новый файл.')
        
        match choose_last_calibration_time:
            case 1:
                data_calibration_date_in_future = analyzer.last_calibration_future()
                df3 = data_calibration_date_in_future
            case 2:
                data_calibration_date_in_past = analyzer.last_calibration_past()
                df3 = data_calibration_date_in_past
            case 3:
                data_calibration_date_is_incorrect = analyzer.last_calibration_incorrect()
                df3 = data_calibration_date_is_incorrect
            case _:
                print('Такого варианта нет.')
                
        print('Сделана страница с датами калибровок.')
        print('----------------------------------------------------------------------')

        df4 = analyzer.create_pivot_table()
        analyzer.dataframes_to_excel([df1, df2, df3, df4], ['filtered_warranty', 'sorted_devices_issues', 'calibration_dates', 'table'], self.__count)
        

    def user_choices(
        self, 
        choice_warranty_until_filter: int = 1, 
        choose_last_calibration_time: int = 1, 
        count_of_clinics: int = 1
    ) -> None:
        """Перебор всех Excel файлов и применение к каждому функции для анализа.
        
        Args:
            choice_warranty_until_filter: пользовательский ввод для выбора типа фильтрации даты последней гарантии мед устройств.
            choose_last_calibration_time: пользовательский ввод для выбора временного отрезка последней калибровки медицинского устройства.
            count_of_clinics: пользовательский ввод для выбора количества клиник, для которых нужно увидеть количество проблем.
        """

        tasks = [self.process_of_analysing(analyzer, choice_warranty_until_filter, choose_last_calibration_time, count_of_clinics) for analyzer in self.__analysing_devices]
        