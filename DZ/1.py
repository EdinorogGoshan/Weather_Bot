import os
import argparse

paramParser = argparse.ArgumentParser()
paramParser.add_argument('-n', '--name', default='Аноним', help='Имя пользователя')
paramParser.add_argument('-p', '--path', default='./text.txt', help='Путь к файлу')
paramParser.add_argument('-y', '--yes', action='store_true', help='Подавление вопросов пользователю')

param = paramParser.parse_args()

name = param.name
path = param.path
doAllThinks = param.yes


def delete_file():
    if os.path.exists(path):
        os.remove(path)
        print(f'Файл "{path}" успешно удален')
    else:
        print('Файл по заданному пути не найден')


def question():
    if not doAllThinks:
        ask = input(f'Удалить файл "{path}"? (y/n): ')
        if ask != 'y':
            return False
    return True


print("Приветствую " + name)

if question():
    delete_file()
