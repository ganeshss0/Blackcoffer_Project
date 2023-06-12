import requests as R
import os
import math
from bs4 import BeautifulSoup as BS
from src.utility import read_excel, get_response_wrapper, File_Path, html_parser
from src.logger import logging
from src.exception import CustomException
import multiprocessing as mp


class Extraction:
    def __init__(self):
        logging.info('Data Extraction Started')
        self.path = os.path.join('Data', 'Raw_Text')
        os.makedirs(self.path, exist_ok=True)


    def load_data(self, FilePath: str = File_Path, *args, **kwargs):
        data = read_excel(FilePath, *args, **kwargs)
        self.data = data


    def get_data(self):
        for i in range(0, self.data.shape[0], 10):
            with mp.Pool() as pool:
                pool.map(get_response_wrapper, self.data.iloc[i:i+10])


    def extract_text(self):
        for root, folder, files in os.walk(self.path):
            for file in files:
                path = os.path.join(root, file)
                with open(path) as file:
                    parsed = html_parser(file.read())
                    paragraphs = parsed.findAll('p')
                with open(path, 'w') as file:
                    [file.write(paragraph.text) for paragraph in paragraphs]
            

        

