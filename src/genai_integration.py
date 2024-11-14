from azure.ai.textanalytics import TextAnalyticsClient, ExtractiveSummaryAction
from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential
import os
from dotenv import load_dotenv

load_dotenv('secrets.env') 

# Azure Text Analytics Credentials 
azure_api_key = os.environ.get("AZURE_TEXT_ANALYTICS_KEY") 
azure_endpoint = os.environ.get("AZURE_TEXT_ANALYTICS_ENDPOINT") 
# 
# Azure Search Credentials 
service_endpoint = os.environ.get("AZURE_SEARCH_ENDPOINT") 
index_name = os.environ.get("AZURE_SEARCH_INDEX") 
key = os.environ.get("AZURE_SEARCH_API_KEY")

# Initialize Azure Text Analytics Client
def authenticate_client():
    ta_credential = AzureKeyCredential(azure_api_key)
    text_analytics_client = TextAnalyticsClient(
        endpoint=azure_endpoint,
        credential=ta_credential
    )
    return text_analytics_client

def extract_medical_insights(document_text):
    """Extract key medical insights from the document."""
    client = authenticate_client()
    response = client.begin_analyze_healthcare_entities(documents=[document_text])
    result = response.result()
    docs = [doc for doc in result if not doc.is_error]
    insights = {
        "Dosage": [],
        "MedicationName": []
    }
    for idx, doc in enumerate(docs):
        for entity in doc.entities:
            if "Dosage" in entity.category and entity.text not in insights["Dosage"]:
                insights["Dosage"].append(entity.text)
            elif "MedicationName" in entity.category:
                insights["MedicationName"].append(entity.text)
    return insights

def search_documents(query):
    """Search for medical documents based on a query."""
    search_client = SearchClient(
        endpoint=service_endpoint,
        index_name=index_name,
        credential=AzureKeyCredential(key)
    )

    results = search_client.search(search_text=query)
    return [result for result in results]

def analyze_document(document_text):
    """Analyze document text using Azure's AI services."""
    client = authenticate_client()
    response = client.extract_key_phrases(documents=[document_text])[0]

    if not response.is_error:
        return response.key_phrases
    else:
        return f"Error: {response.error}"

def summarize_document(document_text):
    """Generate a summary of the document using Azure Text Analytics."""
    client = authenticate_client()
    response = client.begin_analyze_actions(documents=[document_text],
                                      actions=[ExtractiveSummaryAction(max_sentence_count=2)],)
    document_results = response.result()
    for result in document_results:
        extract_summary_result = result[0]  # first document, first result
        if extract_summary_result.is_error:
            print("...Is an error with code '{}' and message '{}'".format(
                extract_summary_result.code, extract_summary_result.message
            ))
        else:
            return("\n{}".format(
                " ".join([sentence.text for sentence in extract_summary_result.sentences]))
            )

if __name__ == "__main__":
    # Sample analysis to test the setup
    
    sample_text = "The patient was given instruction on use of nasal saline irrigation to be used twice daily and Clarinex 5 mg daily was recommended."
    insights = extract_medical_insights(sample_text)
    print(f"Extracted Medical Insights: {insights}")
    
    """ TESTING FOR EXTRACTIVE SUMMARIZATION
    sample_text = "Patient's report shows a history of hypertension and diabetes. Recent symptoms include severe headache and dizziness. Prescribed medication includes Metformin and Lisinopril."
    summary = summarize_document(sample_text)
    print(f"Summary: {summary}")
    """
    
    
    """ TESTING FOR SEARCH FEATURE
        search_results = search_documents("cardiovascular")
        for result in search_results:
        print(f"Content: {result['content']}")"""
