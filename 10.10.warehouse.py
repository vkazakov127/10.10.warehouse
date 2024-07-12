# -*- coding: utf-8 -*-
# 10.10.warehouse.py
import multiprocessing as mp
from datetime import datetime


class WarehouseManager:

    def __init__(self, w_data):
        self.w_data = w_data

    def process_request(self, w_request):
        product = w_request[0]
        action = w_request[1]
        quantity = w_request[2]
        print(f'{product}; {action}; {quantity}.')
        # Принимаем / отгружаем товар
        if action == 'receipt':
            if product in self.w_data:
                self.w_data[product] += quantity
            else:
                self.w_data[product] = quantity
        elif action == 'shipment':
            if product in self.w_data:
                quantity1 = self.w_data[product]
                if quantity1 < quantity:
                    print(f'Невозможно отгрузить {product}:{quantity}. В наличии {quantity1}')
                else:
                    self.w_data[product] -= quantity
            else:
                print(f'Невозможно отгрузить товар: {product}. Он отсутствует на Складе')
        else:
            print(f'Неправильный тип Операции: {action}. Доступные типы: "receipt", "shipment". ')
        # Товар на складе. Результат операции "action".
        print(f'Товар на складе. PROCESS_REQUEST: {self.w_data}')

    def run(self, w_requests_lst):
        for request1 in w_requests_lst:  # по списку запросов
            self.process_request(request1)
        # Товар на складе. Результат после выполнения всех запросов.
        print(f'Товар на складе. RUN: {self.w_data}')


if __name__ == '__main__':
    with mp.Manager() as manager:
        # Начало творения склада
        warehouse_data = manager.dict()
        w_manager = WarehouseManager(warehouse_data)
        # Список запросов
        requests = [
            ("product1", "receipt", 100),
            ("product2", "receipt", 150),
            ("product1", "shipment", 30),
            ("product3", "receipt", 200),
            ("product2", "shipment", 50)
        ]
        # Засекаем время
        time1 = datetime.now()
        # ---------
        # Вариант БЕЗ процессов
        # w_manager.run(requests)
        # ---------
        # Вариант с Процессами
        with mp.Pool(processes=5) as my_pool:
            # Тут идут процессы, 5 штук
            my_pool.map(w_manager.run, (requests,))             # Можно так — как написано в Задании
            # my_pool.map(w_manager.process_request, requests)  # Можно и вот так
        # ---------
        # Засекаем время
        time2 = datetime.now()
        duration = time2 - time1
        print(f'Время работы приложения = {duration}')

        # Товар на складе. Результат после выполнения всех запросов.
        print(f'Товар на складе. The End 01: {w_manager.w_data}')
        # То же самое, другим макаром
        print(f'Товар на складе. The End 02: {warehouse_data}')
        print('---------- The End ----------')
