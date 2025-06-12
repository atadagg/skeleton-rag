from abc import ABC, abstractmethod
import os
from typing import List

# Add Google Drive API imports
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google.oauth2 import service_account
import io

class DataSource(ABC):
    @abstractmethod
    def fetch(self):
        """Fetch data from the source."""
        pass

class GithubFetcher(DataSource):
    def __init__(self, credentials):
        self.credentials = credentials

    def fetch(self):
        # TODO: Implement GitHub data fetching
        pass

class GoogleDriveFetcher(DataSource):
    def __init__(self, credentials_json: str, folder_id: str):
        self.credentials_json = credentials_json
        self.folder_id = folder_id
        self.service = self.authenticate()

    def authenticate(self):
        """Authenticate with Google Drive using a service account JSON file."""
        SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
        credentials = service_account.Credentials.from_service_account_file(
            self.credentials_json, scopes=SCOPES)
        service = build('drive', 'v3', credentials=credentials)
        return service

    def fetch(self) -> List[dict]:
        """Fetch file metadata and content from the specified Google Drive folder."""
        results = self.service.files().list(
            q=f"'{self.folder_id}' in parents and trashed=false",
            pageSize=1000,
            fields="files(id, name, mimeType)"
        ).execute()
        files = results.get('files', [])
        fetched_files = []
        for file in files:
            file_id = file['id']
            file_name = file['name']
            mime_type = file['mimeType']
            # Only fetch text-based files for this example
            if mime_type == 'application/vnd.google-apps.document':
                # Export Google Docs as plain text
                request = self.service.files().export_media(fileId=file_id, mimeType='text/plain')
                fh = io.BytesIO()
                downloader = MediaIoBaseDownload(fh, request)
                done = False
                while not done:
                    status, done = downloader.next_chunk()
                content = fh.getvalue().decode('utf-8')
            else:
                # For other files, try to download as binary
                request = self.service.files().get_media(fileId=file_id)
                fh = io.BytesIO()
                downloader = MediaIoBaseDownload(fh, request)
                done = False
                while not done:
                    status, done = downloader.next_chunk()
                content = fh.getvalue()
            fetched_files.append({
                'id': file_id,
                'name': file_name,
                'mime_type': mime_type,
                'content': content
            })
        return fetched_files

def get_data_sources(config):
    sources = []
    for src in config["sources"]:
        if src["type"] == "github":
            sources.append(GithubFetcher(src["credentials"]))
        elif src["type"] == "gdrive":
            sources.append(GoogleDriveFetcher(src["credentials_json"], src["folder_id"]))
        # Add more elifs for new sources
    return sources 