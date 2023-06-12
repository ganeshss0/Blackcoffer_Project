import pandas as pd
import requests as R
from bs4 import BeautifulSoup as BS
from src.logger import logging
from src.exception import CustomException

import sys
import os

File_Path = os.path.join('Data', 'Input.xlsx')

def read_excel(FilePath: str, *args, **kwargs) -> pd.DataFrame:
    if os.path.exists(File_Path):
        try:
            logging.info('Loading Data')
            df = pd.read_excel(io = FilePath, *args, **kwargs)
            logging.info('Loading Data Succesfully')
            return df
        except:
            logging.error('Loading Data Failed')
            raise CustomException('Loading Data Failed', sys)
    else:
        logging.error('Path does not exists or Input.xlsx is missing')
        raise CustomException('Invalid Path or Input.xlsx is missing!', sys)



    
def get_response(url: str, *args, **kwargs) -> R.Response:
        """Return a response object based on the input url.\n
        Arguments:
            * url -> URL of a website, example: 'https://en.wikipedia.com'"""
        
        logging.info(f'Sending request to {url}')
        try:
            response = R.get(url)
            logging.info('Receive Response Succesful')
        except ConnectionError:
            logging.error('Request Failed')
            raise CustomException('Requests Failed', sys)
        
        return response.text


def html_parser(markup: str) -> BS:
    '''Convert string into a Parsed HTML object.'''
    
    return BS(markup, 'html.parser')

def html_tag_finder(html_parsed: BS, tag_name: str, identifier: dict = {}) -> 'list[BS]':
    '''Return a list of matching HTML tags from a Soup Object.'''
    
    tags = html_parsed.findAll(tag_name, identifier)
    string = ''
    for tag in tags:
        paragraphs = tag.findAll('p')
        for paragraph in paragraphs:
            string += paragraph.text
    return string