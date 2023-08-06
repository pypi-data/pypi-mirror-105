#!/usr/bin/env python
# coding: utf-8

# Aim: Implement functions that allow user to work with google drive.

from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from mimetypes import MimeTypes

from datetime import datetime
import sys, os, math
import pandas as pd

class GoogleDrive(object):
    """
    Class allows for programmatic:
        - Uploading of files to Google Drive
        - Listing of all files & folders available to a service account.
        - Sharing of files with a list of email addresses.
        
    This code has been modified from the version found here:
        https://gist.github.com/rajarsheem/1d9790f0e9846fb429d7
    This code has been tested on V3 of the google drive api found here:
        https://developers.google.com/drive/api/v3/about-sdk
    """
    def __init__(self):
        # Recommended: Use the 'create_credentials' function below to overwrite the credentials below.
        # This helps avoid having to pass the credentials parameter into each of the subsequent functions.
        self.credentials = None
        
    def create_credentials(self, service_account_json_filename):
        """
        Function creates service account credentials used to authenticate Google Drive requests.
        A service account credentials json object is used as a authenticator.
        See links for details:
            https://cloud.google.com/iam/docs/creating-managing-service-accounts#iam-service-accounts-create-console
            https://support.google.com/a/answer/7378726?hl=en

        Parameters:
            service_account_json_filename - a string with the full path & name to a .json object that authenticates a 
            service account.
            E.g: '/Users/luyanda.dhlamini/Projects/client_secrets.json'

        Returns:
            credentials - Google Service Account credentials object of type:
               oauth2client.service_account.ServiceAccountCredentials
        """
        assert '.json' in service_account_json_filename, 'Ensure that your service account filename is a json file.'

        # create credenntials used to access google services.
        credentials = ServiceAccountCredentials.from_json_keyfile_name(filename=service_account_json_filename)

        return credentials


    def upload_file_to_google_drive(self, path, credentials=None, parent_id=None):
        """
        Upload a file to a google drive folder.

        Parameters:
            path - The full/absolute string path to a file.
                E.g: '/Users/luyanda.dhlamini/Projects/Customer Maturity Model/2021_02_07_customer_classification_1.csv'
            credentials - Google Service Account credentials object of type:
               oauth2client.service_account.ServiceAccountCredentials. Default: None
            parent_id - The item used to identify which folder to place a file in. Default: None.
                The root / home Drive folder is used if parent_id = None
                E.g: 'https://drive.google.com/drive/folders/1czCX8xlhkPyxu00000UbEqncVOPX0000'

        Returns:
            file_id_dict - a dictionary with the id of the uploaded file.
        """
        if self.credentials is not None:
            credentials = self.credentials

        mime = MimeTypes()
        service = build('drive', 'v3', credentials=credentials)

        file_metadata = {
            'name': os.path.basename(path),
        }
        if parent_id:
            file_metadata['parents'] = [parent_id]

        media = MediaFileUpload(path,
                                mimetype=mime.guess_type(os.path.basename(path))[0],
                                resumable=True)

        file_id_dict = service.files().create(body=file_metadata,
                                  media_body=media,
                                  fields='id').execute()

        return file_id_dict

    def list_files_in_google_drive(self, credentials=None):
        """
        List files that are available to a google drive service account.
        NB: The files shown are files that are available TO THE SERVICE ACCOUNT and not necessarily those of the person
        running this code.

        Parameters:
            credentials - Google Service Account credentials object of type:
               oauth2client.service_account.ServiceAccountCredentials. Default: None

        Returns:
            item_dict - A dictionary with a google drive acount's file details.
        """
        if self.credentials is not None:
            credentials = self.credentials

        service = build('drive', 'v3', credentials=credentials)
        results = service.files().list(fields="nextPageToken, files(id, name,mimeType)").execute()
        items = results.get('files', [])
        item_dict = {'name':[],'id':[]}
        if not items:
            print('No files found.')
        else:

            for item in items:
                item_dict['name'].append(item['name'])
                item_dict['id'].append(item['id'])
            print('Total files found:', len(items))
        return item_dict

    def share_google_drive_file(self, file_id, emails, credentials = None, role = 'writer'):
        """
        Share a google drive file with email address accounts.
        See link below for available role options:
            https://developers.google.com/drive/api/v3/ref-roles
        Parameters:
            file_id - A string unique identifier to a google drive file.
            emails - A list of email addresses to share a file with.
            credentials - Google Service Account credentials object of type:
               oauth2client.service_account.ServiceAccountCredentials. Default: None
            role - The user permissions type to assign to a user with access to a file. Default: 'writer'.

        Returns:
            results - A dictionary with the results of sharing files with user email addresses. 
        """
        def callback(request_id, response, exception):
            if exception:
                # Handle error
                print(exception)

        if self.credentials is not None:
            credentials = self.credentials

        results = {'User':[],'Role':[]}
        service = build('drive', 'v3', credentials=credentials)
        batch = service.new_batch_http_request(callback=callback)
        for user in emails:
            user_permission = {
                'type': 'user',
                'role': role,
                'emailAddress': user
            }

            batch.add(service.permissions().create(
                fileId=file_id,
                body=user_permission,
                fields='id',
            ))
            batch.execute()
            results['User'].append(user)
            results['Role'].append(role)

        return results











# Example
# Here we create & upload a text file to the service acount's default Drive folder





# Create a file path to the current directory


if __name__ == "__main__":
    # This is an example of how to use this package.
    
    # Find the path that this script is running from.
    file_path = os.path.abspath('.') + '/'
    print('file_path:',file_path)

    # Instantiate the GoogleDrive class
    gdrive = GoogleDrivePython()

    # Store the name of the service account json file in a variable. 
    # Replace the name below with your service account's filename
    service_account_name = 'client_secrets.json'

    # Add the service account name to your current directory path.
    service_account_name_full_path = file_path + service_account_name
    print("service_account_name:", service_account_name_full_path)

    # Create credentials using the create_credentials function
    credentials = gdrive.create_credentials(service_account_json_filename = service_account_name_full_path)

    # Overwrite the class's default credentials with the newly created credentials.
    gdrive.credentials = credentials

    # The code below would be used if we wanted to upload the file to an exsting google drive folder.
    # parent_folder_id = '1czCX8xlhkPyxuDl3gnUbEqncVO000000'
    # parent_folder_url = 'https://drive.google.com/drive/folders/{}'.format(parent_folder_id)
    # print(parent_folder_url)

    # Create & save a text file into the local directory
    test_file = "test_file.txt"
    f = open(test_file, "w")
    f.write("Test Content")
    f.close()

    # Add the text file above to the current directory's path.
    file_to_upload = test_file
    file_to_upload_full_path = file_path + file_to_upload
    print('File to upload:', file_to_upload_full_path)

    # Upload the text file created above to google drive
    # Storing it's file_id in a variable
    file_id_dict = gdrive.upload_file_to_google_drive(path=file_to_upload_full_path)

    # View the returned file id info.
    print(file_id_dict)

    # Get the id from the newly created file dictionary object
    file_id = file_id_dict['id']

    # Write down the email address(es) to share the file with in a list.
    email_list = ['johnsmith@gmail.com', 'luyandedlamini@gmail.com', 'rajarsheem@gmail.com']

    # Share the file with the email address list.
    share_results = gdrive.share_google_drive_file(file_id=file_id, emails=email_list)
    print(share_results)

    # Get all files & folders available to the service account into a dictionary.
    all_files_dict = gdrive.list_files_in_google_drive()

    # Print & view the available file, folder names and ids.
    # The newly created text file should also appear in the output.
    print(all_files_dict)

    # You may use the ids of any of the files/ folders for additional operations.

