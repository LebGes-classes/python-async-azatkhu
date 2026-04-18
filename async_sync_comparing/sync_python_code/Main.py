from Menu import Menu

import asyncio
import time
import os


if __name__ == '__main__':

    menu = Menu()
    menu.choose_filter_warranty_option()
    choice_warranty_until_filter = int(input())
    menu.choose_calibration_time()
    choose_last_calibration_time = int(input())
    count_of_clinics = int(input('Введите количество клиник, для которых хотите увидеть количество проблем.'))
    start = time.time()
    menu.user_choices(choice_warranty_until_filter, choose_last_calibration_time, count_of_clinics)
    sync_code_execution_time = time.time() - start
    with open('result_to_compare.txt', 'a', encoding = 'utf-8') as f:
        f.write('синхронно_выполненный_код: ' + str(sync_code_execution_time) + '\n')

    print(f'Программа проработала {sync_code_execution_time} секунд.')
