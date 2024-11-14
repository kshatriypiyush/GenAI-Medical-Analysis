# GenAI Medical Document Analysis

## Overview
The GenAI Medical Document Analysis project leverages Azure AI services to perform advanced analysis on medical documents. The application can extract key medical insights, generate summaries, and provide search functionality to find relevant information in medical reports.

## Features
- **Medical Insight Extraction**: Extracts Dosage and Medication data from medical documents.
- **Summarization**: Generates concise summaries of medical reports for quick review.
- **Search Functionality**: Enables users to search over medical documents to find relevant information.

## Setup

### Prerequisites
- Python 3.7 or higher
- Git

### Project Structure

genai-medical-analysis/ ├── data/ │ └── sample_medical_reports/ ├── src/ │ ├── data_preprocessing.py │ └── genai_integration.py ├── venv/ │ ├── bin/ │ ├── include/ │ ├── lib/ │ └── ... ├── app.py ├── README.md └── requirements.txt


### Installation

1. **Clone the repository:**
   ```sh
   git clone https://github.com/kshatriypiyush/GenAI-Medical-Analysis.git
   cd genai-medical-analysis

2. **Create and activate a virtual environment:**
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`

3. **Install the required packages:**
   ```sh
   pip install -r requirements.txt

4. **Install the required packages:**
   AZURE_TEXT_ANALYTICS_KEY=Your Azure Language Key
   AZURE_TEXT_ANALYTICS_ENDPOINT=Your Azure Language Endpoint
   AZURE_SEARCH_API_KEY=Your Azure Search Key
   AZURE_SEARCH_ENDPOINT=Your Search Endpoint
   AZURE_SEARCH_INDEX=Index Name

## Usage

1. **Clone the repository:**
   ```sh
   python app.py

2. **Open the application in your browser: Navigate to http://127.0.0.1:8050/ to access the DASH interface.**

3. **Upload Medical Documents:**
   ```sh
   Drag and drop or select a file to upload. View extracted insights and summaries.

4. **Search Medical Documents:**
   ```sh
   Use the search bar to query medical documents. View search results with highlighted keywords and relevant information.


## Testing

1. **Extract Medical Insights:**
   ```sh
   from src.genai_integration import extract_medical_insights
   sample_text = "The patient was given instruction on use of nasal saline irrigation to be used twice daily and Clarinex 5 mg daily was recommended."
   insights = extract_medical_insights(sample_text)
   print(f"Extracted Medical Insights: {insights}")

2. **Summarize Document:**
   ```sh
   from src.genai_integration import summarize_document
   sample_text = "Patient's report shows a history of hypertension and diabetes. Recent symptoms include severe headache and dizziness. Prescribed medication includes Metformin and Lisinopril."
   summary = summarize_document(sample_text)
   print(f"Summary: {summary}")

3. **Search Documents:**
   ```sh
   from src.genai_integration import search_documents
   search_results = search_documents("cardiovascular")
   for result in search_results:
   print(f"Document ID: {result['id']}, Content: {result['content']}")


## Contributing
We welcome contributions! Please follow these steps:

1. **Fork the repository.**

2. **Create a feature branch:**
   ```sh
   git checkout -b feature-name

3. **Commit your changes:**
   ```sh
   git commit -m 'Add some feature'

4. **Push to the branch:**
   ```sh
   git push origin feature-name

5. **Open a pull request.**

## License

**This project is licensed under the MIT License. See the LICENSE file for details.**

## Contact

**If you have any questions or suggestions, feel free to reach out!**

# Happy Coding!