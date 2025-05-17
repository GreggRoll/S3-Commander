import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output, State
import dash_uploader as du
import boto3
import pandas as pd

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
du.configure_upload(app, r"/tmp/uploads")

# S3 Configuration
s3_client = boto3.client('s3')
bucket_name = 'your-s3-bucket-name'

# Country-City Data
country_city_data = {
    "N/A": ["N/A"],
    "Country1": ["City1", "City2"],
    "Country2": ["City3"]
}

# Layout Components
navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dcc.Dropdown(
            id='country-dropdown',
            options=[{'label': k, 'value': k} for k in country_city_data.keys()],
            value='N/A'
        )),
        dbc.NavItem(dcc.Dropdown(
            id='city-dropdown',
            options=[{'label': 'N/A', 'value': 'N/A'}],
            value='N/A'
        )),
        dbc.NavItem(dcc.Input(id='search-bar', type='text', placeholder='Search...')),
        dbc.NavItem(dbc.Button("Upload", id="open-upload-modal", color="primary"))
    ],
    brand="S3 Interface Tool",
    brand_href="#",
    color="primary",
    dark=True,
)

upload_modal = dbc.Modal(
    [
        dbc.ModalHeader("Upload Files"),
        dbc.ModalBody([
            dcc.Dropdown(
                id='modal-country-dropdown',
                options=[{'label': k, 'value': k} for k in country_city_data.keys()],
                value='N/A'
            ),
            dcc.Dropdown(
                id='modal-city-dropdown',
                options=[{'label': 'N/A', 'value': 'N/A'}],
                value='N/A'
            ),
            du.Upload(
                id='file-upload',
                text='Drag and Drop or Select Files',
                max_file_size=-1,  # No limit
                filetypes=['any']
            )
        ]),
        dbc.ModalFooter(
            dbc.Button("Upload", id="upload-button", color="primary")
        ),
    ],
    id="upload-modal",
    is_open=False,
)

file_table = dbc.Table(
    id='file-table',
    children=[
        html.Thead(html.Tr([html.Th("Checkbox"), html.Th("Country"), html.Th("City"), html.Th("Name"), html.Th("Size"), html.Th("Date Modified")])),
        html.Tbody(id='file-table-body')
    ],
    bordered=True,
    striped=True,
    hover=True,
)

app.layout = dbc.Container(
    [
        navbar,
        upload_modal,
        html.Br(),
        file_table,
        dbc.Button("Download", id="download-button", color="success"),
        dbc.Button("Delete", id="delete-button", color="danger")
    ],
    fluid=True,
)

# Callbacks for dependent dropdowns in the modal
@app.callback(
    Output('modal-city-dropdown', 'options'),
    Input('modal-country-dropdown', 'value')
)
def set_city_options(selected_country):
    return [{'label': city, 'value': city} for city in country_city_data[selected_country]]

# Callbacks for opening and closing the upload modal
@app.callback(
    Output("upload-modal", "is_open"),
    [Input("open-upload-modal", "n_clicks"), Input("upload-button", "n_clicks")],
    [State("upload-modal", "is_open")]
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open

# Callback for handling file uploads
@du.callback(
    output=Output('file-upload', 'isCompleted'),
    id='file-upload'
)
def upload_files(filenames):
    for filename in filenames:
        # Upload file to S3 with metadata
        country = dash.callback_context.inputs['modal-country-dropdown.value']
        city = dash.callback_context.inputs['modal-city-dropdown.value']
        s3_client.upload_file(
            filename,
            bucket_name,
            filename,
            ExtraArgs={
                'Metadata': {
                    'Country': country,
                    'City': city
                }
            }
        )
    return True

# Callback to update the file table
@app.callback(
    Output('file-table-body', 'children'),
    [Input('country-dropdown', 'value'), Input('city-dropdown', 'value'), Input('search-bar', 'value')]
)
def update_file_table(selected_country, selected_city, search_term):
    response = s3_client.list_objects_v2(Bucket=bucket_name)
    files = response.get('Contents', [])
    
    rows = []
    for file in files:
        metadata = s3_client.head_object(Bucket=bucket_name, Key=file['Key'])['Metadata']
        country = metadata.get('country', 'N/A')
        city = metadata.get('city', 'N/A')
        
        if (selected_country == 'N/A' or selected_country == country) and \
           (selected_city == 'N/A' or selected_city == city) and \
           (not search_term or search_term.lower() in file['Key'].lower()):
            rows.append(html.Tr([
                html.Td(dbc.Checkbox()),
                html.Td(country),
                html.Td(city),
                html.Td(file['Key']),
                html.Td(file['Size']),
                html.Td(file['LastModified'].strftime('%Y-%m-%d %H:%M:%S'))
            ]))
    
    return rows

if __name__ == '__main__':
    app.run_server(debug=True)
