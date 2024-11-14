import base64
import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.dependencies import Input, Output, State
from src.genai_integration import extract_medical_insights, summarize_document, search_documents
from src.data_preprocessing import preprocess_documents
import fitz  # PyMuPDF
import os

# Initialize the DASH app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Define the app layout
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("GenAI Medical Document Analysis", className="text-center my-4"), width=12)
    ]),
    dbc.Row([
        dbc.Col(dcc.Upload(
            id="upload-data",
            children=html.Div([
                "Drag and Drop or ",
                html.A("Select Files")
            ]),
            style={
                "width": "100%",
                "height": "60px",
                "lineHeight": "60px",
                "borderWidth": "1px",
                "borderStyle": "dashed",
                "borderRadius": "5px",
                "textAlign": "center",
                "margin": "10px"
            },
            multiple=False
        ), width={"size": 6, "offset": 3})
    ]),
    dbc.Row([
        dbc.Col(dcc.Loading(
            id="loading",
            type="circle",
            children=html.Div(id="output-insights", className="mt-4")
        ), width=12)
    ]),
    dbc.Row([
        dbc.Col(dcc.Input(
            id="search-input",
            type="text",
            placeholder="Search medical documents...",
            className="form-control mt-4",
            style={"width": "100%"}
        ), width={"size": 6, "offset": 3}),
        dbc.Col(dbc.Button("Search", id="search-button", color="primary", className="mt-4"), width={"size": 2, "offset": 0})
    ]),
    dbc.Row([
        dbc.Col(html.Div(id="search-results", className="mt-4"), width={"size": 10, "offset": 1})
    ])
], fluid=True)

def extract_text_from_pdf(pdf_data):
    """Extract text from PDF file."""
    pdf_document = fitz.open(stream=pdf_data, filetype="pdf")
    text = ""
    for page_num in range(pdf_document.page_count):
        page = pdf_document.load_page(page_num)
        text += page.get_text()
    return text

@app.callback(
    Output("output-insights", "children"),
    Input("upload-data", "contents"),
    State("upload-data", "filename")
)
def update_output(contents, filename):
    if contents is not None:
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)

        # Extract text based on file type
        if filename.lower().endswith(".pdf"):
            document_text = extract_text_from_pdf(decoded)
        else:
            document_text = decoded.decode("utf-8")

        # Preprocess the document text
        processed_text = preprocess_documents([document_text])

        # Join the preprocessed chunks into a single string
        document_text = " ".join(processed_text)

        # Extract insights and summary
        insights = extract_medical_insights(document_text)
        summary = summarize_document(document_text)

        return dbc.Card([
            dbc.CardBody([
                html.H4(f"Extracted Insights from {filename}", className="card-title"),
                html.P(f"Dosage: {', '.join(insights.get('Dosage', []))}", className="card-text"),
                html.P(f"MedicationName: {', '.join(insights.get('MedicationName', []))}", className="card-text"),
                html.H4("Summary", className="mt-3"),
                html.P(summary, className="card-text")
            ])
        ], className="mt-4")

# Define callback to handle search functionality
@app.callback(
    Output("search-results", "children"),
    Input("search-button", "n_clicks"),
    State("search-input", "value")
)
def update_search_results(n_clicks, query):
    if n_clicks is not None and query:
        search_results = search_documents(query)
        return html.Div([
            html.H4("Search Results", className="mt-4"),
            dbc.ListGroup([
                dbc.ListGroupItem([
                    html.P(result['content'], className="mb-1")
                ]) for result in search_results
            ])
        ])
    return ""

if __name__ == "__main__":
    app.run_server(debug=True)
