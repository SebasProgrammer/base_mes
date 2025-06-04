from .instances import config, logger
"""
Source: https://github.com/iamlu-coding/python-sharepoint-office365-api/
"""
from office365.sharepoint.client_context import ClientContext
from office365.runtime.auth.user_credential import UserCredential
from office365.sharepoint.files.file import File
from openpyxl import load_workbook
from io import BytesIO

USERNAME=config['sharepoint']['username']
PASSWORD=config['sharepoint']['password']
SHAREPOINT_SITE=config['sharepoint']['site']
SHAREPOINT_SITE_NAME=config['sharepoint']['site_name']
SHAREPOINT_DOC=config['sharepoint']['doc']

class SharePoint:
  def _auth(self):
    conn = ClientContext(SHAREPOINT_SITE).with_user_credentials(USERNAME, PASSWORD)
    return conn
  
  def _get_files_list(self, folder_name):
    conn = self._auth()
    target_folder_url = f'{SHAREPOINT_DOC}/{folder_name}'
    root_folder = conn.web.get_folder_by_server_relative_url(target_folder_url)
    root_folder.expand(["Files", "Folders"]).get().execute_query()
    return root_folder.files

  def download_file(self, file_name, folder_name):
    conn = self._auth()
    file_url = f'/sites/{SHAREPOINT_SITE_NAME}/{SHAREPOINT_DOC}/{folder_name}/{file_name}'
    file = File.open_binary(conn, file_url)
    return file.content
    
  def upload_file(self, file_name, folder_name, content):
    conn = self._auth()
    target_folder_url = f'/sites/{SHAREPOINT_SITE_NAME}/{SHAREPOINT_DOC}/{folder_name}'
    target_folder = conn.web.get_folder_by_server_relative_path(target_folder_url)
    response = target_folder.upload_file(file_name, content).execute_query()
    return response

  def download_file_locally(self, file_name, folder_name, download_path):
    conn = self._auth()
    file_url = f'/sites/{SHAREPOINT_SITE_NAME}/{SHAREPOINT_DOC}/{folder_name}/{file_name}'
    file = File.open_binary(conn, file_url)
    logger.info(f'file_url:\n\t {file_url}')
    wb = load_workbook(BytesIO(file.content))
    wb.save(download_path)
    wb.close()