
# Power BI Report Performance Data Collection Script

## Overview

This script automates the process of collecting performance data for Power BI report pages using Selenium. It logs into Power BI, navigates through specified report pages, collects performance metrics, and stores the data in a CSV file. 

## Prerequisites

- Python 3.x
- Google Chrome installed
- ChromeDriver (automatically installed via `chromedriver_autoinstaller`)
- Required Python packages: `selenium`, `pandas`, `chromedriver-autoinstaller`
- Access to the reports with a user account

## Setup

### 1. Install Required Python Packages

Use a package manager like pip to install the required Python packages: selenium, pandas, chromedriver-autoinstaller, msal, requests

### 2. Credentials

Ensure that you use the credentials of the users with the access to the reports.



### 3. Collecting Report and Page Information

Use Power BI REST  API  script pbi_reportPages.py or get the data from Power BI Monitoring SQL DB  to generate the `power_bi_reports_pages.csv` file, which contains information about the Power BI reports and pages to be analyzed. 

The CSV file should have the following structure:

- workspace_id
- report_id
- report_name
- page_id
- page_name
- url
You can also use the data from Power BI Monitoring Solution. Download simply the needed data from the DB. In practice you want to run the performance analysis on the most used reports or the reports used by the VIP users. 


### 4. Main Performance Data Collection Script

Save the main performance data collection script to a file (e.g., `collect_performance_data.py`). This script will read the `power_bi_reports_pages.csv` file, navigate through each report page, collect performance data, and save it to a new CSV file.

### Running the Script

To run the script, use your Python interpreter to execute the script file.

### Output

The script will create a CSV file named `power_bi_performance_data.csv` with the collected performance data.
You can load the data to Power BI and have the clear results of the performance of the reports in your PBI service.
![obraz](https://github.com/AstralForest/Power_BI_Service_Perfomance_Tracking/assets/103418860/cae69a25-681a-446a-b819-a2d4b02c6f6e)


## Troubleshooting

- Ensure that the CSV file is correctly formatted and accessible.
- Verify that the environment variables are set correctly.
- Check for any issues with ChromeDriver installation or permissions.

## Best Practices

- **Error Handling**: The script includes basic error handling to catch and report any issues during execution.
- **Dynamic Waiting**: Use WebDriverWait instead of fixed sleep intervals to make the script more reliable and efficient.
- **Resource Management**: Ensure that the browser is properly closed after the script execution to free up system resources.

## License

This script is provided "as-is" without any warranty. Use at your own risk.

## Next Steps

I recommend to use this script and register the data from it once per month so you can build the robust history of the performance of your top reports. It's good to run this scripts 2 times in a row. If there is no active cache on a given report page, it will be created and used the next time the report is opened. If the difference in the display times of a given page is significant, it means that caches were not created during the first iteration of the code.

You can get the most value from the performance information once you mix this data together with the information about the most used reports in your organization. 

## Authors

- Michal Debski (michal.debski@astralforest.com)

---

This README provides comprehensive instructions and best practices for using and maintaining the script. Ensure to update the environment variables and test the script in a controlled environment before deploying it in production.
