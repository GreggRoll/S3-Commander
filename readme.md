S3 Interface Tool Development Plan
Project Overview
The S3 Interface Tool is a web application built using Dash that provides a graphical user interface (GUI) for interacting with Amazon S3 buckets. The application will leverage the boto3 library for S3 operations and the dash-uploader package to handle file uploads without size limitations. The tool will feature a navigation bar with country and city filters, a search bar, and an upload button. Users can upload files with associated metadata and manage files within the S3 bucket through a table interface.

Requirements Collection
User Interface (UI) Requirements:

Navigation Bar:
Dropdown for selecting Country (default: All)
Dropdown for selecting City (default: All)
Search bar for filtering files
Upload button to open a modal for file uploads
Upload Modal:
Fields for selecting Country and City (dependent dropdowns)
File upload area supporting multiple files
Upload button to initiate the upload process
Main Page:
Table displaying files with columns: Checkbox, Country, City, Name, Size, Date Modified
Buttons for downloading and deleting selected files
Functional Requirements:

File Upload:
Use dash-uploader to handle file uploads without size limitations
Collect metadata (Country and City) during the upload process
Upload files to the S3 bucket with attached metadata
File Management:
List files from the S3 bucket in a table format
Allow users to filter files by Country, City, and search terms
Enable file download and deletion through table actions
Technical Requirements:

Backend:
Use boto3 for S3 operations (upload, list, download, delete)
Store metadata (Country, City) with each file in S3
Frontend:
Use Dash for the web application framework
Implement dependent dropdowns for Country and City using a predefined dictionary
Ensure the application is responsive and user-friendly
Development Outline
Project Setup:

Initialize a new Dash application
Set up virtual environment and install necessary packages (dash, dash-uploader, boto3, etc.)
Navigation Bar Implementation:

Create dropdowns for Country and City with default values
Implement a search bar for filtering files
Add an upload button that triggers the upload modal
Upload Modal Implementation:

Design the modal layout with fields for Country and City
Implement dependent dropdowns for Country and City using the provided dictionary
Integrate dash-uploader for file uploads
Add an upload button to initiate the file upload process
File Upload Handling:

Configure dash-uploader to handle large file uploads
Implement backend logic to upload files to S3 with metadata (Country, City)
Ensure metadata is stored and retrievable from S3
Main Page Table Implementation:

Design a table to display files with columns: Checkbox, Country, City, Name, Size, Date Modified
Fetch and list files from the S3 bucket
Implement filtering based on Country, City, and search terms
File Management Actions:

Implement download functionality for selected files
Implement delete functionality for selected files
Testing and Validation:

Test the application for various use cases (file upload, filtering, download, delete)
Validate the functionality of dependent dropdowns and metadata handling
Ensure the application handles large files efficiently
