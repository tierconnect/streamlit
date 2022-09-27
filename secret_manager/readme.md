# Secret Manager
This part of the project will handle the upload and retrieve process of the secrets into Google Secret Manager

## Disclaimer
All the information in this repository is private. The credentials, URLs and keys defined in the 
JSON files in the folders can be retrieved securely from any of the Streamlit applications in this folder. 

Do not use credentials in Streamlit. Use always the Secret Manager to retrieve them on runtime. 

## Upload
Edit the json files in `resources/environment/credentials.json`. 
Create a pull request, get it approved, and it's ready.

## Read a Secret
To read a secret, check the Streamlit app template in this repository.
