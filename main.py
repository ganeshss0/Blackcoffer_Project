from src.components.data_extraction import Extraction
from src.logger import logging
from src.components.sentimental_analysis import Analysis
from src.utility import output_file_name

if __name__ == '__main__':
    app = Extraction()
    app.load_data()
    app.get_data()
    app.extract_text()
    logging.info('Data Extraction Succesful')
    RawText = app.data.TEXT.copy()
    analysis = Analysis()
    analysis.preprocess_text(app.data)
    analysis.remove_stopwords(app.data)
    analysis.extract_derived_variable(app.data)
    analysis.readability_analysis(RawText, app.data)
    analysis.text_statistics(app.data)
    logging.info('Analysis Succesful')
    app.data.drop(columns=['TEXT'], inplace=True)
    output_file = output_file_name()
    app.data.to_excel(output_file, index=False)
    logging.info(f'Analysis Results saved at {output_file}')    

