import requests as R
import os
from bs4 import BeautifulSoup as BS
from src.utility import read_excel, get_response, File_Path, html_parser, html_tag_finder
from src.logger import logging
from src.exception import CustomException


class Extraction:
    def __init__(self):
        logging.info('Data Extraction Started')
        self.path = os.path.join('Data', 'Raw_Text')
        os.makedirs(self.path, exist_ok=True)


    def load_data(self, FilePath: str = File_Path, *args, **kwargs):
        data = read_excel(FilePath, *args, **kwargs)
        self.data = data.head(10)


    def get_data(self):
        logging.info(f'Fetching {self.data.shape[0]} Links')
        RESPONSE = self.data.URL.apply(get_response)
        self.PARSED  = RESPONSE.apply(html_parser)
        logging.info(f'Fetching {self.data.shape[0]} Links Succesfully')


    def extract_text(self):
        self.data['TEXT'] = self.PARSED.apply(html_tag_finder, args=('div', {'class' : 'td-post-content tagdiv-type'}))