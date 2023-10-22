# CSV-Importer

### I had used the python and streamlit framework to build the web app which can be used as CSV Importer

### To create the API Key for Google Sheet
- Go to Google Developers Console
- Create the new project and go to project dashboard
- Search for Google Drive API and Google Sheets API and enable them
- Click on create credentials and select the parameters
- Enter the service account name and select role
- Go to IAM and admin from the menu and select service accounts
- Go to keys section and click on add key->create new key with key type as json

### Project Procedure
- Clone the repository and install the required libraries from requirements.txt file
- Move to the project directory and type command "streamlit run csv_importer.py"
- Create the new google sheets and mention the same name in web app along with the json file
- Copy the client email address displayed in the web app and paste it in the share section of google sheet with role as editor
-  After selecting and filtering the columns with the help of the web app, click the button "Convert" to trigger the action.

### Output Video

https://github.com/StackItHQ/stackit-hiring-assignment-Krishshrk/assets/93509656/b8c16705-0ec9-4e4b-b075-4fc8ad982630
