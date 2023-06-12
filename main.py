from src.components.data_extraction import Extraction

if __name__ == '__main__':
    start = Extraction()
    start.load_data()
    start.get_data()
    start.extract_text()