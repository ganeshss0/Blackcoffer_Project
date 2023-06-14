from src.utility import read_excel, get_response, File_Path, html_parser, html_tag_finder
from src.logger import logging



class Extraction:
    '''Main Extraction Class'''


    def __init__(self) -> None:
        logging.info('Data Extraction Started')


    def load_data(self, FilePath: str = File_Path, *args, **kwargs) -> None:
        '''Read the Excel file.'''
        
        data = read_excel(FilePath, *args, **kwargs)
        self.data = data


    def get_data(self) -> None:
        '''Sending request to URL and parsing response into html parser.'''

        logging.info(f'Fetching {self.data.shape[0]} Links')
        RESPONSE = self.data.URL.apply(get_response)
        self.PARSED  = RESPONSE.apply(html_parser)
        logging.info(f'Fetching {self.data.shape[0]} Links Succesfully')


    def extract_text(self) -> None:
        '''Extract Text data from parsed html.'''

        self.data['TEXT'] = self.PARSED.apply(html_tag_finder, args=('div', {'class' : 'td-post-content tagdiv-type'}))