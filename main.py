from src.components.data_extraction import Extraction
import os

if __name__ == '__main__':
    app = Extraction()
    app.load_data()
    app.get_data()
    app.extract_text()
    app.data.to_excel(os.path.join('Data', 'Output.xlsx'), index=False)