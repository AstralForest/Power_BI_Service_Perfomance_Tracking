from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import chromedriver_autoinstaller
import time
import pandas as pd

# Automatically install chromedriver if not available
chromedriver_autoinstaller.install()

# Configure Chrome options
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')
options.add_argument('--auto-open-devtools-for-tabs')

# Start the browser
service = Service()
driver = webdriver.Chrome(service=service, options=options)

# Load credentials from environment variables
email = os.getenv('POWERBI_EMAIL', 'your email')
password = os.getenv('POWERBI_PASSWORD', 'your password')

# Open Power BI and log in
driver.get('https://app.powerbi.com/')
time.sleep(2)

email_field = driver.find_element(By.ID, 'email')
email_field.send_keys(email)
email_field.send_keys(Keys.RETURN)
time.sleep(2)

password_field = driver.find_element(By.NAME, 'passwd')
password_field.send_keys(password)
password_field.send_keys(Keys.RETURN)
time.sleep(25)

# Read the CSV file containing report and page information
csv_file_path = 'power_bi_reports_pages.csv'
reports_pages_df = pd.read_csv(csv_file_path)
print(reports_pages_df)

# Initialize an empty DataFrame to store all performance data
all_performance_data = pd.DataFrame()

# Function to hover and close tabs
def hover_and_close_tabs(driver):
    while True:
        try:
            # Get all tri-navbar-tab-item elements
            navbar_tab_items = driver.find_elements(By.CSS_SELECTOR, 'tri-navbar-tab-item[data-testid^="navbarItem"]')
            
            if not navbar_tab_items:
                print("No more tabs found.")
                break

            for navbar_tab_item in navbar_tab_items:
                try:
                    # Hover over the tri-navbar-tab-item element
                    actions = ActionChains(driver)
                    actions.move_to_element(navbar_tab_item).perform()

                    # Wait until the close button within the current tab item is present and clickable
                    close_button = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-testid="tab-close"]'))
                    )

                    # Click on the close button
                    close_button.click()

                    # Wait for the tab to be removed
                    WebDriverWait(driver, 10).until(EC.staleness_of(navbar_tab_item))

                    # Break after closing one tab to re-fetch the list
                    break

                except Exception as e:
                    print(f"An error occurred while processing a tab: {e}")

        except Exception as e:
            print(f"An error occurred: {e}")
            break

# Function to collect performance data for a report page
def collect_performance_data(driver, report_url, workspace_id, report_id, page_name, pass_number):
    try:
        # Navigate to the report page
        driver.get(report_url)
        time.sleep(2)  # Adjust the wait time as needed

        # Start performance tracing
        driver.execute_script('window.performance.mark("start");')

        # Wait for a while to allow the page to load
        WebDriverWait(driver, 120).until(lambda d: d.execute_script('return document.readyState') == 'complete')

        # Stop performance tracing and collect data
        driver.execute_script('window.performance.mark("end");')
        driver.execute_script('window.performance.measure("duration", "start", "end");')
        performance_data = driver.execute_script('return window.performance.getEntriesByType("measure");')

        # Convert performance data to DataFrame
        df = pd.DataFrame(performance_data)

        # Convert startTime and duration to seconds with 2 decimals
        df['startTime'] = (df['startTime'] / 1000).round(2)
        df['duration'] = (df['duration'] / 1000).round(2)

        # Add additional columns with report, page information, and pass number
        df['workspace_id'] = workspace_id
        df['report_id'] = report_id
        df['page_name'] = page_name
        df['timestamp'] = time.strftime('%Y-%m-%d %H:%M:%S')
        df['pass'] = pass_number

        return df

    except Exception as e:
        print(f"An error occurred while processing {report_url} on pass {pass_number}: {e}")
        return pd.DataFrame()  # Return an empty DataFrame in case of error

# Loop through each report page listed in the CSV
for index, row in reports_pages_df.iterrows():
    workspace_id = row['workspace_id']
    report_id = row['report_id']
    page_name = row['page_name']
    report_url = row['url']
    
    print(f"Processing row {index}, {report_url} - Pass 1")
    df_pass1 = collect_performance_data(driver, report_url, workspace_id, report_id, page_name, 1)
    all_performance_data = pd.concat([all_performance_data, df_pass1], ignore_index=True)
    
    print(f"Processing row {index}, {report_url} - Pass 2")
    df_pass2 = collect_performance_data(driver, report_url, workspace_id, report_id, page_name, 2)
    all_performance_data = pd.concat([all_performance_data, df_pass2], ignore_index=True)
    
    # Call the function to hover and close tabs after each pass
    hover_and_close_tabs(driver)

# Export all performance data to a CSV file
output_csv_path = "power_bi_performance_data.csv"
all_performance_data.to_csv(output_csv_path, index=False)

# Close the browser
driver.quit()
