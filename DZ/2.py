import os
import argparse

import pickle


class Data:
    def __init__(self, name='Anonim', surname='Anonim') -> None:
        self.name = name
        self.surname = surname


dataArray = []

paramParser = argparse.ArgumentParser()
paramParser.add_argument('-f', '--file', default='ini', help='Название файла конфигурации')
param = paramParser.parse_args()

fileName = param.file
dirPath = 'Settings/'
filePath = f"{dirPath}{fileName}"
filePathDefault = f"{dirPath}ini"

if not os.path.exists(filePathDefault) or not os.path.getsize(filePathDefault) > 0:
    if not os.path.exists(dirPath):
        os.makedirs(dirPath)
    for i in range(10):
        data = Data()
        data.surname += f' {i}'
        dataArray.append(data)
    with open(filePathDefault, "wb") as dataFile:
        pickle.dump(dataArray, dataFile)
    print('Создан файл настроек, в него записаны элементы:')
    for data in dataArray:
        print(f'{data.name}; {data.surname}')
else:
    with open(filePathDefault, "rb") as dataFile:
        dataArray = pickle.load(dataFile)
    print('Из файла настроек прочтены элементы:')
    for data in dataArray:
        print(f'{data.name}; {data.surname}')

with open(filePath, "wb") as dataFile:
    pickle.dump(dataArray, dataFile)
    print('\nСоздан новый файл настроек, в него записаны элементы:')
    for data in dataArray:
        print(f'{data.name}; {data.surname}')
