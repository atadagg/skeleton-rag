from abc import ABC, abstractmethod
import os
from typing import List, Dict, Optional
import requests

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
    """
    Fetches files from a GitHub repository. Easily configurable for different repos, branches, paths, and file types.
    """
    def __init__(self, credentials: dict, repo: str, branch: str = "main", path: str = "", extensions: Optional[List[str]] = None):
        """
        credentials: dict with 'token' key for GitHub personal access token
        repo: 'owner/repo' string
        branch: branch name (default 'main')
        path: subdirectory in the repo (default root)
        extensions: list of file extensions to include (e.g., ['.md', '.py'])
        """
        self.token = credentials.get("token")
        self.repo = repo
        self.branch = branch
        self.path = path
        self.extensions = extensions or []

    def fetch(self) -> List[Dict]:
        """Fetch all files matching the filter from the repo, recursively."""
        headers = {"Authorization": f"token {self.token}"} if self.token else {}
        return list(self._walk_and_fetch(self.path, headers))

    def _walk_and_fetch(self, path: str, headers: dict):
        for item in self._list_dir(path, headers):
            if item["type"] == "file" and self._should_include(item["name"]):
                yield self._fetch_file(item, headers)
            elif item["type"] == "dir":
                yield from self._walk_and_fetch(item["path"], headers)

    def _list_dir(self, path: str, headers: dict) -> List[Dict]:
        url = f"https://api.github.com/repos/{self.repo}/contents/{path}?ref={self.branch}"
        resp = requests.get(url, headers=headers)
        if resp.status_code != 200:
            print(f"GitHub API error: {resp.status_code} {resp.text}")
            return []
        return resp.json()

    def _should_include(self, filename: str) -> bool:
        return not self.extensions or any(filename.endswith(ext) for ext in self.extensions)

    def _fetch_file(self, file_info: Dict, headers: dict) -> Dict:
        resp = requests.get(file_info["download_url"], headers=headers)
        if resp.status_code != 200:
            print(f"Failed to fetch {file_info['download_url']}: {resp.status_code}")
            return {}
        return {
            "name": file_info["name"],
            "path": file_info["path"],
            "content": resp.text,
            "sha": file_info["sha"],
            "download_url": file_info["download_url"]
        }

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
            sources.append(GithubFetcher(src["credentials"], src["repo"], src["branch"], src["path"], src["extensions"]))
        elif src["type"] == "gdrive":
            sources.append(GoogleDriveFetcher(src["credentials_json"], src["folder_id"]))
        # Add more elifs for new sources
    return sources 