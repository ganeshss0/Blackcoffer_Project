from src.components.data_extraction import Extraction

if __name__ == '__main__':
    start = Extraction()
    start.load_data()
    start.get_data()
    start.extract_text()
    start.data.to_csv('./Data_extraction.csv')