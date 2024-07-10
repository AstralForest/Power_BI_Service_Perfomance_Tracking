import msal
import requests
import pandas as pd

# Authentication details provide the necessary information from your app registration 
client_id = ''
client_secret = ''
tenant_id = ''

# Power BI workspace IDs - provide the list of the workspaces you want to scrap the data from in order to list the Reports and Reportages from them
workspace_ids = [
    'workspaceid1',
    'workspaceid2'
]

# Authenticate and get access token
authority = f"https://login.microsoftonline.com/{tenant_id}"
scope = ["https://analysis.windows.net/powerbi/api/.default"]

app = msal.ConfidentialClientApplication(client_id, authority=authority, client_credential=client_secret)
token_response = app.acquire_token_for_client(scopes=scope)
access_token = token_response.get('access_token')

headers = {
    'Authorization': f'Bearer {access_token}'
}

# DataFrame to store the results
data = []

for workspace_id in workspace_ids:
    # Get reports in the workspace
    reports_url = f"https://api.powerbi.com/v1.0/myorg/groups/{workspace_id}/reports"
    reports_response = requests.get(reports_url, headers=headers)
    
    if reports_response.status_code == 200:
        reports = reports_response.json().get('value')
        
        for report in reports:
            report_id = report['id']
            report_name = report['name']
            
            # Get pages in the report
            pages_url = f"https://api.powerbi.com/v1.0/myorg/groups/{workspace_id}/reports/{report_id}/pages"
            pages_response = requests.get(pages_url, headers=headers)
            
            if pages_response.status_code == 200:
                pages = pages_response.json().get('value')
                
                for page in pages:
                    page_id = page['name']
                    page_display_name = page['displayName']
                    page_url = f"https://app.powerbi.com/groups/{workspace_id}/reports/{report_id}/{page_id}"
                    
                    # Add to the data list
                    data.append([workspace_id, report_id, report_name, page_id, page_display_name, page_url])
            else:
                print(f"Failed to get pages for report {report_name} in workspace {workspace_id}. Error: {pages_response.text}")
    else:
        print(f"Failed to get reports for workspace {workspace_id}. Error: {reports_response.text}")

# Create a DataFrame
df = pd.DataFrame(data, columns=['Workspace ID', 'Report ID', 'Report Name', 'Page ID', 'Page Name', 'URL'])

# Save DataFrame to CSV
df.to_csv('power_bi_reports_pages.csv', index=False)
