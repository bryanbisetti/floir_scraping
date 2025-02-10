import time
import concurrent.futures
import os
import shutil
import csv
import ast
import re

import pandas as pd

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options

# ad number of tries to the tuple, and as long as it increase, increase the time of sleep 5 -> 10 -> 20 -> 30 -> 50
def download_report(year, quarter, county, coverage, n, sleep_time, count_error_connection = 0):
    # Set up Selenium WebDriver
    # Configure options
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    combination = (year, quarter, county, coverage, n, sleep_time)

    # Set a custom download directory
    download_directory = f"/Users/bibbi/Desktop/RA/all_reports/{n}"  # Change to your desired location
    os.makedirs(download_directory, exist_ok=True) 
    prefs = {
        "download.default_directory": download_directory,  # Directory for downloads
        "download.prompt_for_download": False,            # Disable "Save As" dialog
        "download.directory_upgrade": True,               # Upgrade directory permissions
        "safebrowsing.enabled": True                      # Enable safe browsing
    }
    options.add_experimental_option("prefs", prefs)

    # Create the WebDriver (Selenium Manager automatically handles driver setup)
    driver = webdriver.Chrome(options=options)
    driver.set_page_load_timeout(150)

    try:
        # Open QSRNG interactive tools page
        driver.get("https://apps.fldfs.com/QSRNG/Reports/ReportCriteriaWizard.aspx")
        wait = WebDriverWait(driver, 20)

        # Wait for the page to fully load
        wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body')))

        # first page
        MS_dropdown = driver.find_element(By.XPATH, '//select[@id="ctl00_ContentPlaceHolder1_ddlCustomReport"]')
        Select(MS_dropdown).select_by_visible_text('Market Share')

        time.sleep(1)

        #second page
        button = driver.find_element(By.XPATH, '//input[@id="ctl00_ContentPlaceHolder1_btnMSNext"]')
        button.click()

        time.sleep(1)

        # third page
        year_dropdown = driver.find_element(By.XPATH, '//select[@id="ctl00_ContentPlaceHolder1_ddlFilingYear"]')
        Select(year_dropdown).select_by_visible_text(year)
        button = driver.find_element(By.XPATH, '//input[@id="ctl00_ContentPlaceHolder1_btnFilingYear"]')
        button.click()

        time.sleep(1)

        #forth page
        button = driver.find_element(By.XPATH, '//input[@id="ctl00_ContentPlaceHolder1_btnFilingType"]')
        button.click()

        time.sleep(1)

        #fifth page
        MS_dropdown = driver.find_element(By.XPATH, '//select[@id="ctl00_ContentPlaceHolder1_lstReportingPeriod_LeftBox"]')
        Select(MS_dropdown).select_by_visible_text(quarter)
        button = driver.find_element(By.XPATH, '//input[@id="ctl00_ContentPlaceHolder1_lstReportingPeriod_MoveRight"]')
        button.click()

        time.sleep(1)
        
        button = driver.find_element(By.XPATH, '//input[@id="ctl00_ContentPlaceHolder1_btnReportingPeriod"]')
        button.click()

        time.sleep(sleep_time-5)

        # sixt page (include also 'All')
        MS_dropdown = driver.find_element(By.XPATH, '//select[@id="ctl00_ContentPlaceHolder1_lstCounties_LeftBox"]')
        Select(MS_dropdown).select_by_visible_text(county)
        button = driver.find_element(By.XPATH, '//input[@id="ctl00_ContentPlaceHolder1_lstCounties_MoveRight"]')
        button.click()

        time.sleep(sleep_time-5) # there is some gap between the arrow click and the county name movement

        button = driver.find_element(By.XPATH, '//input[@id="ctl00_ContentPlaceHolder1_btnCounty"]')
        button.click()

        time.sleep(3)

        # sevent page
        MS_dropdown = driver.find_element(By.XPATH, '//select[@id="ctl00_ContentPlaceHolder1_lstInsurers_LeftBox"]')
        Select(MS_dropdown).select_by_visible_text('All')
        button = driver.find_element(By.XPATH, '//input[@id="ctl00_ContentPlaceHolder1_lstInsurers_MoveRight"]')
        button.click()

        time.sleep(sleep_time-5) # there is some gap between the arrow click and the All movement

        button = driver.find_element(By.XPATH, '//input[@id="ctl00_ContentPlaceHolder1_btnInsurer"]')
        button.click()

        time.sleep(3)

        # eight page (include also 'All')
        MS_dropdown = driver.find_element(By.XPATH, '//select[@id="ctl00_ContentPlaceHolder1_lstPolicyType_LeftBox"]')
        Select(MS_dropdown).select_by_visible_text(coverage)
        button = driver.find_element(By.XPATH, '//input[@id="ctl00_ContentPlaceHolder1_lstPolicyType_MoveRight"]')
        button.click()

        time.sleep(sleep_time-5) # there is some gap between the arrow click and the All movement

        button = driver.find_element(By.XPATH, '//input[@id="ctl00_ContentPlaceHolder1_btnPolicyType"]')
        button.click()

        time.sleep(3)

        # ninth page
        MS_dropdown = driver.find_element(By.XPATH, '//select[@id="ctl00_ContentPlaceHolder1_lstDataElements_LeftBox"]')
        Select(MS_dropdown).select_by_visible_text('All')
        button = driver.find_element(By.XPATH, '//input[@id="ctl00_ContentPlaceHolder1_lstDataElements_MoveRight"]')
        button.click()

        time.sleep(2) # there is some gap between the arrow click and the All movement

        button = driver.find_element(By.XPATH, '//input[@id="ctl00_ContentPlaceHolder1_btnDataElement"]')
        button.click()

        time.sleep(85)

        # tenth page
        # Wait for new tab or page to open (if applicable)
        WebDriverWait(driver, 10).until(lambda d: len(d.window_handles) > 1)

        # Get all open windows/tabs
        all_windows = driver.window_handles

        driver.switch_to.window(all_windows[1])

        # eleventh page
        button = driver.find_element(By.XPATH, '//div[@id="rptViewer_ctl05_ctl04_ctl00"]')
        button.click()
        time.sleep(1)
        button = driver.find_element(By.XPATH, '//a[@title="Excel"]')
        button.click()

        time.sleep(15)

        driver.quit()
        print(f'{combination} done correctly!')
        return 'Correct', None

    except Exception as e:
        driver.quit()
        error_message = str(e)
        if 'Message: unknown error: net::ERR_CONNECTION_RESET' in error_message and count_error_connection == 0:
            print('Retry after connection reset')
            return download_report(year, quarter, county, coverage, n, sleep_time, count_error_connection = 1)
        print(f'{combination} Error: {e}')
        return 'Error', combination


def crate_items_combination_list():
    coverages = [
    "All",
    "Commercial Residential - (Apartment Buildings) - WIND ONLY",
    "Commercial Residential - (Condo Associations Only) - WIND ONLY",
    "Commercial Residential - (Homeowners Association) - WIND ONLY",
    "Commercial Residential - Allied Lines (Condo Associations Only)",
    "Commercial Residential - Allied Lines (Excl Condo Associations)",
    "Commercial Residential - CMP (Condo Associations Only)",
    "Commercial Residential - CMP (Excl Condo Associations)",
    "Commercial Residential - Dwelling/Fire (Condo Associations Only)",
    "Commercial Residential - Dwelling/Fire (Excl Condo Associations)",
    "Personal Residential - Allied Lines",
    "Personal Residential - Allied Lines - WIND ONLY DWELLINGS",
    "Personal Residential - Condominium Unit Owners",
    "Personal Residential - Condominium Unit Owners - WIND ONLY",
    "Personal Residential - Dwelling/Fire",
    "Personal Residential - Dwelling/Fire - Mobile Homeowners",
    "Personal Residential - Dwelling/Fire - Mobile Homeowners - WIND ONLY",
    "Personal Residential - Excess Private Flood",
    "Personal Residential - Farmowners",
    "Personal Residential - Homeowners (Excl Tenant and Condo) - Owner Occupied",
    "Personal Residential - Homeowners (Excl Tenant and Condo) - Owner Occupied - WIND ONLY",
    "Personal Residential - Mobile Homeowners",
    "Personal Residential - Mobile Homeowners - WIND ONLY",
    "Personal Residential - Primary Private Flood",
    "Personal Residential - Tenants",
    "Personal Residential - Tenants - WIND ONLY"
    ]
    counties = [
    "All", "Alachua", "Baker", "Bay", "Bradford", "Brevard", "Broward", "Calhoun",
    "Charlotte", "Citrus", "Clay", "Collier", "Columbia", "Dade", "Desoto", "Dixie",
    "Duval", "Escambia", "Flagler", "Franklin", "Gadsden", "Gilchrist", "Glades", "Gulf",
    "Hamilton", "Hardee", "Hendry", "Hernando", "Highlands", "Hillsborough", "Holmes", "Indian River",
    "Jackson", "Jefferson", "Lafayette", "Lake", "Lee", "Leon", "Levy", "Liberty",
    "Madison", "Manatee", "Marion", "Martin", "Monroe", "Nassau", "Okaloosa", "Okeechobee",
    "Orange", "Osceola", "Palm Beach", "Pasco", "Pinellas", "Polk", "Putnam", "Santa Rosa",
    "Sarasota", "Seminole", "St. Johns", "St. Lucie", "Sumter", "Suwannee", "Taylor", "Union",
    "Volusia", "Wakulla", "Walton", "Washington"
    ]

    years = ['2024', '2023', '2022', '2021', '2020', '2019', '2018', '2017', '2016', '2015', '2014', '2013', '2012', '2011', '2010', '2009']
    count = 0
    final_list = []
    for year in years:
        quarters = [f'Quarter 1 (01/01/{year}-03/31/{year})', f'Quarter 2 (04/01/{year}-06/30/{year})', f'Quarter 3 (07/01/{year}-09/30/{year})', f'Quarter 4 (10/01/{year}-12/31/{year})']
        for quarter in quarters:
            for county in counties:
                for coverage in coverages:
                    count += 1
                    final_list.append((year,quarter,county, coverage,count, 10))

    # # Specify the CSV file name
    # csv_file_inputs = "inputs.csv"

    # # Write the list of dictionaries to the CSV file
    # with open(csv_file_inputs, mode='w', newline='') as file:
    #     writer = csv.writer(file)
    #     writer.writerow(['tuple'])  # Header row

    #     # Write each dictionary as a string
    #     for tuple in final_list:
    #         writer.writerow([str(tuple)])

    # print(f"CSV file '{csv_file_inputs}' created successfully!")
    # pd.read_csv(csv_file_inputs)


def parallelize_scraping(inputs_list):
    # Maximum number of threads to use in parallel
    queue = []
    max_threads = 20  # Adjust based on your system's capabilities
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_threads) as executor:
        # Submit each task to the ThreadPool
        futures = [executor.submit(download_report, year, quarter, county, coverage, n, sleep_time) for year, quarter, county, coverage, n, sleep_time in inputs_list]
        
        for future in concurrent.futures.as_completed(futures):
            try:
                result, combination = future.result()  # Get result of the future
                if result == 'Error':
                    queue.append(combination)
            except Exception as e:
                print(f"Exception occurred: {e}")
        return queue


def rename_and_save_excel_files():
    # Input directory containing the Excel files
    input_directory = "/Users/bibbi/Desktop/RA/all_reports"
    # Output base directory for structured files
    output_directory = "/Users/bibbi/Desktop/RA/final_reports"
    forgotten_elements = list()

    for item in os.listdir(input_directory):
        if not item.isdigit():
            continue
        initial_directory = os.path.join(input_directory, item)
        filename = 'MarketShareTsExternal.xlsx'
        file_path = os.path.join(initial_directory, filename)
        print(file_path)

        try:
            window = pd.read_excel(file_path, engine = 'openpyxl')

            reporting_period = window.iloc[5,7] # from reporting_period extract year and quarter
            year = reporting_period.split('/')[2].split('-')[0]
            quarter = reporting_period.split('/')[0].split(' ')[1]
            quarter = f"Q{quarter}"

            policy_type = window.iloc[6,7] # extract policy
            policy = policy_type.replace(' - ', '_').replace('/', '_')

            county = window.iloc[7,7] # extract county

            new_filename = f"mktshare_{year}{quarter}_{county}_{policy}.xlsx"

            year_quarter_county_dir = os.path.join(output_directory, year, quarter, county)
            os.makedirs(year_quarter_county_dir, exist_ok=True)  # Create directories if they don't exist
            new_file_path = os.path.join(year_quarter_county_dir, new_filename)
            if os.path.exists(new_file_path): # Check if the file already exists
                print(f"File already exists: {new_file_path}. Skipping...")
                shutil.rmtree(initial_directory)
                continue
            os.rename(file_path, new_file_path)
            print(f"Renamed and moved: {filename} -> {new_file_path}")
            shutil.rmtree(initial_directory)
            
        except Exception as e:
            print(f"Error processing {filename}: {e}")
            forgotten_elements.append(int(item))
            shutil.rmtree(initial_directory)

        if item in os.listdir(input_directory):
            forgotten_elements.append(int(item))
            shutil.rmtree(initial_directory)

    return list(set(forgotten_elements))


def open_csv():
    with open('inputs.csv', mode='r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        tuples = [ast.literal_eval(row[0]) for row in reader]
    return tuples


def modify_csv(queue_errors, start_number, total_number, forgotten_elements):

    with open("inputs.csv", mode='r') as file:
        reader = csv.reader(file)
        header = next(reader)  # Read the header
        data = [ast.literal_eval(row[0]) for row in reader]  # Convert strings to tuples

    error_data = [item for item in data[start_number:total_number] if item in queue_errors or int(item[-2]) in forgotten_elements]
    
    # correct sleep time
    new_error_data = []
    for tupla in error_data:
        new_tupla = list(tupla)
        new_tupla[-1] = min(30,new_tupla[-1]+5)
        new_error_data.append(tuple(new_tupla))
    
    final_list = data[:start_number] + new_error_data + data[total_number:]

    # save new csv
    with open("inputs.csv", mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['tuple'])  # Header row

        # Write each dictionary as a string
        for tupla in final_list:
            writer.writerow([str(tupla)])
    print('CSV corrected!')