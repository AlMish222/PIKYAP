from dataclasses import dataclass
from typing import List, Dict

from main import files


# Класс "Файл" с количественным признаком "Каталог файлов"
@dataclass
class File:
    file_id: int
    file_name: str
    file_volume: int
    file_directory_id: int  # Для связи 1:M

# Класс "Каталог файлов"
@dataclass
class FileDirectory:
    file_directory_id: int
    name: str

# Промежуточный класс "Файл в Каталоге файлов" для связи М:М
@dataclass
class FileInTheFileDirectory:
    file_id: int
    file_directory_id: int

# Запрос 1: Список всех файлов с их объёмами и файловыми каталогами, отсортированный по файловым каталогам
def list_files_in_the_directory(files: List[File], fileDirectories: List[FileDirectory]) -> List[tuple]:
    result = []
    for file_directory in sorted(fileDirectories, key=lambda fd: fd.name):
        for file in filter(lambda f: f.file_directory_id == file_directory.file_directory_id, files):
            result.append((file.file_name, file.file_volume, file_directory.name))
    return result

# Запрос 2: Список файловых каталогов с суммарным размером файлов, отсортированный по объёму файлов
def list_file_directories_with_total_file_volume(files: List[File], fileDirectories: List[FileDirectory]) -> List[tuple]:
    file_volume = {fileDirectory.file_directory_id: 0 for fileDirectory in fileDirectories}
    for file in files:
        file_volume[file.file_directory_id] += file.file_volume
    sorted_fileDirectories = sorted(fileDirectories, key=lambda fd: file_volume[fd.file_directory_id], reverse=True)
    return [(fileDirectory.name, file_volume[fileDirectory.file_directory_id]) for fileDirectory in sorted_fileDirectories]

# Запрос 3: Список каталогов с файлами, если в названии каталога есть слово "язык"
def list_directories_with_files_with_keyword(fileDirectories: List[FileDirectory], fileInTheFileDirectories: List[FileInTheFileDirectory], files: List[File], keyword: str = "язык") -> Dict[str, List[str]]:
    result = {}
    for fileDirectory in filter(lambda fd: keyword in fd.name.lower(), fileDirectories):
        result[fileDirectory.name] = [
            next(f for f in files if f.file_id == link.file_id).file_name
            for link in filter(lambda ffd: ffd.file_directory_id == fileDirectory.file_directory_id, fileInTheFileDirectories)
        ]
    return result

import unittest
from main2 import File, FileDirectory, FileInTheFileDirectory, list_files_in_the_directory, list_file_directories_with_total_file_volume, list_directories_with_files_with_keyword

class TestFileFunctions(unittest.TestCase):
    def setUp(self):
        self.fileDirectories = [
    FileDirectory(file_directory_id=1, name="Английский язык"),
    FileDirectory(file_directory_id=2, name="Математика"),
    FileDirectory(file_directory_id=3, name="Языки программирования"),
    FileDirectory(file_directory_id=4, name="Правоведение"),
]
        self.files = [
    File(file_id=1, file_name="Пересказ модуль 1", file_volume=10, file_directory_id=1),
    File(file_id=2, file_name="Пересказ модуль 3", file_volume=15, file_directory_id=1),

    File(file_id=3, file_name="ДЗ 1", file_volume=20, file_directory_id=2),
    File(file_id=4, file_name="ДЗ 2", file_volume=45, file_directory_id=2),
    File(file_id=5, file_name="РК 1", file_volume=16, file_directory_id=2),

    File(file_id=6, file_name="Лабораторная работа 1", file_volume=12, file_directory_id=3),
    File(file_id=7, file_name="Телеграм бот", file_volume=37, file_directory_id=3),

    File(file_id=8, file_name="ДЗ на 30.10", file_volume=35, file_directory_id=4),
    File(file_id=9, file_name="КР 2", file_volume=70, file_directory_id=4),
    File(file_id=10, file_name="Лекция №3", file_volume=110, file_directory_id=4),
    File(file_id=11, file_name="Лекция №7", file_volume=12, file_directory_id=4),
]
        self.fileInTheFileDirectories = [
    FileInTheFileDirectory(file_id=1, file_directory_id=1),
    FileInTheFileDirectory(file_id=2, file_directory_id=1),

    FileInTheFileDirectory(file_id=3, file_directory_id=2),
    FileInTheFileDirectory(file_id=4, file_directory_id=2),
    FileInTheFileDirectory(file_id=5, file_directory_id=2),

    FileInTheFileDirectory(file_id=6, file_directory_id=3),
    FileInTheFileDirectory(file_id=7, file_directory_id=3),

    FileInTheFileDirectory(file_id=8, file_directory_id=4),
    FileInTheFileDirectory(file_id=9, file_directory_id=4),
    FileInTheFileDirectory(file_id=10, file_directory_id=4),
    FileInTheFileDirectory(file_id=11, file_directory_id=4),
]
    def test_list_files_in_the_directory(self):
        result = list_files_in_the_directory(self.files, self.fileDirectories)
        self.assertEqual(result[0], ('Пересказ модуль 1', 10, 'Английский язык'))

    def test_list_file_directories_with_total_file_volume(self):
        result = list_file_directories_with_total_file_volume(self.files, self.fileDirectories)
        self.assertEqual(result[0], ('Правоведение', 227))

    def test_list_directories_with_files_with_keyword(self):
        result = list_directories_with_files_with_keyword(self.fileDirectories, self.fileInTheFileDirectories, self.files)
        self.assertTrue('Английский язык' in result)