import os
import json
from typing import Optional
from google.oauth2 import service_account
from googleapiclient.discovery import build
from langchain_core.tools import tool

SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
SERVICE_ACCOUNT_FILE = 'service_account.json'

def get_drive_service():
    """Authenticates and returns the Google Drive API service instance using an environment variable."""
    # 1. Get the JSON string from the environment
    service_account_info_str = os.environ.get('GCP_SERVICE_ACCOUNT_JSON')
    
    if not service_account_info_str:
        raise ValueError("GCP_SERVICE_ACCOUNT_JSON environment variable is missing.")
        
    # 2. Parse the string back into a Python dictionary
    service_account_info = json.loads(service_account_info_str)
    
    # 3. Use from_service_account_info instead of from_service_account_file
    creds = service_account.Credentials.from_service_account_info(
        service_account_info, scopes=SCOPES)
        
    return build('drive', 'v3', credentials=creds)

@tool
def search_google_drive(query_string: str) -> str:
    """
    Searches Google Drive using a valid 'q' parameter string. 
    Examples:
    - name = 'Project.pdf' (Exact name)
    - name contains 'Report' (Partial name)
    - mimeType = 'application/pdf' (PDFs)
    - fullText contains 'Machine Learning' (Inside files)
    - modifiedTime > '2024-01-01T00:00:00' (After a date)
    """
    service = get_drive_service()
    try:
        results = service.files().list(
            q=f"{query_string} and trashed = false",
            spaces='drive',
            fields='nextPageToken, files(id, name, mimeType, webViewLink)',
            pageSize=10
        ).execute()
        
        items = results.get('files', [])
        if not items: return f"No files found for: {query_string}"
        
        output = f"Results for query [{query_string}]:\n"
        for item in items:
            output += f"- {item.get('name')} ({item.get('mimeType')}) | {item.get('webViewLink')}\n"
        return output
    except Exception as e:
        return f"Error: {str(e)}"