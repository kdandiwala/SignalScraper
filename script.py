from selenium import webdriver
import os
from pathlib import Path
import time
import glob
import warnings
import sys


warnings.filterwarnings("ignore",  message = "executable_path has been deprecated, please pass in a Service object")

# upload/download variables
downloads = Path("INSERT DOWNLOAD PATH HERE")

# Chrome options for headless version
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--mute-audio")
chrome_prefs = {"download.default_directory": str(downloads)}
chrome_options.experimental_options["prefs"] = chrome_prefs
driver = webdriver.Chrome('INSERT CHROMEDRIVER PATH HERE',  options=chrome_options)
original_window = driver.current_window_handle

categories = {
    1 : "Military",
    2 : "Aviation",
    3 : "Satellite",
    4 : "Radar",
    5 : "Marine",
    6 : "Navigation",
    7 : "Active",
    8 : "Inactive",
    9 : "Analogue",
    10 : "Amateur_Radio",
    11 : "Trunked_Radio",
    12 : "Numbers_Stations",
    13 : "Commercial",
    14 : "Utility",
    15 : "Time"
}

frequencies = {
    1 : "VLF",
    2 : "LF",
    3 : "MF",
    4 : "HF",
    5 : "VHF",
    6 : "UHF"
}

def create_signal_type_folder():
    try:
        signal_type = driver.find_element("xpath", '//*[@id="firstHeading"]/span').text
        signal_type_folder_path = os.path.join(str(downloads), signal_type)
        os.mkdir(signal_type_folder_path)
        print("Signal Type -- " + signal_type)
        return signal_type_folder_path
    except Exception as ex:
        print("Could not create signal type folder: " + str(ex))
        driver.quit()
        sys.exit(1)

def create_signal_folder(xpath, parent_directory):
    try:
        signal = driver.find_element("xpath", xpath).text
        if '/' in signal:
            signal = signal.replace('/', '-')
        print("Downloading signal: " + signal)
        signal_folder_path = os.path.join(parent_directory, signal)
        os.mkdir(signal_folder_path)
        return signal_folder_path
    except Exception as ex:
        print("Could not create signal type folder: " + str(ex))
        driver.quit()
        sys.exit(1)

def get_file_name():
    try:
        list_of_files = glob.glob(str(downloads / "*"))
        latest_file = max(list_of_files, key=os.path.getctime)
        file = Path(latest_file)
        return str(file.name)
    except Exception as ex:
        print("Could not get most recent file: " + str(ex))
        driver.quit()
        sys.exit(1)

def num_rows_cols(table):
    try:
        rows = 1+len(driver.find_elements("xpath",
            '//*[@id="mw-content-text"]/'+table+'/tbody/tr'))
        cols = len(driver.find_elements("xpath",
            '//*[@id="mw-content-text"]/'+table+'/tbody/tr/th'))
        return rows, cols
    except Exception as ex:
        print("Could not retrieve number of rows and cols: " + str(ex))
        driver.quit()
        sys.exit(1)

def download_audio(row, table):
    try:
        audio_html = driver.find_element("xpath",
            '//*[@id="mw-content-text"]/'+table+'/tbody/tr['+str(row)+']/td[8]').get_attribute('innerHTML')

        if audio_html == '—':
            return ''
        index1 = audio_html.find('"')
        audio_html = audio_html[index1+1:len(audio_html)]
        index2 = audio_html.find('"')
        audio_html = audio_html[0:index2]

        driver.switch_to.new_window('tab')
        driver.get(audio_html)


        # The code to download the file

        driver.execute_script('''
            // Javascript Code to create the anchor tag and download the file
            let aLink = document.createElement("a");
            let videoSrc = document.querySelector("video").firstChild.src;
            aLink.href = videoSrc;
            aLink.download = "";
            aLink.click();
            aLink.remove();
        ''')
        time.sleep(0.5)
        driver.close()
        driver.switch_to.window(original_window)
        audio_name = get_file_name()
        return audio_name
    except Exception as ex:
        print("Error when downloading: " + str(ex))
        driver.quit()
        sys.exit(1)

#Handles input and goes to requested url
def create_url():
    while True:
        choice1 = input('Categories (1) or Frequencies (2): ')
        if choice1 == str(1):
            print(
            '''
(1) Military
(2) Aviation
(3) Satellite
(4) Radar
(5) Marine
(6) Navigation
(7) Active
(8) Inactive
(9) Analogue
(10) Amateur Radio
(11) Trunked Radio
(12) Numbers_Stations
(13) Commercial
(14) Utility
(15) Time
(16) Unidentified Signals
            ''')
            cat = input("Enter a number: ")
            if not cat.isdigit():
                print("Not a number")
                continue
            if int(cat) == 16:
                return "https://www.sigidwiki.com/wiki/Template:DatabaseUNID"
            if int(cat) in categories:
                return "https://www.sigidwiki.com/wiki/Category:" + categories[int(cat)]
            else:
                print("Invalid number")
                continue

        elif choice1 == str(2):
            print(
            '''
(1) Very Low Frequency
(2) Low Frequency
(3) Medium Frequency
(4) High Frequency
(5) Very High Frequency
(6) Ultra High Frequency
            ''')
            freq = input("Enter a number: ")
            if not freq.isdigit():
                print("Not a number")
                continue
            if int(freq) in frequencies:
                return "https://www.sigidwiki.com/wiki/Category:" + frequencies[int(freq)]
            else:
                print("Invalid number")
                continue
        else:
            print("Please enter 1 or 2")

def main():
    try:
        url = create_url()
        if "Template" in url:
            table = "table"
        else:
            table = "table[2]"
        driver.get(url)
        parent = create_signal_type_folder()
        rows, cols = num_rows_cols(table)
        for r in range(2, 6):
            audio_name = download_audio(r, table)
            if audio_name == '':
                time.sleep(1)
                signal = driver.find_element("xpath", '//*[@id="mw-content-text"]/'+table+'/tbody/tr['+str(r)+']/td[1]').text
                print("Download for " + signal + " skipped -- no audio file available")
                continue
            folder = create_signal_folder('//*[@id="mw-content-text"]/'+table+'/tbody/tr['+str(r)+']/td[1]', parent)
            os.replace('/Users/krish/Desktop/project/' + audio_name, folder + '/' + audio_name)
        print("Finished")
    except Exception as ex:
        print("Error in main: " + str(ex))
        driver.quit()
        sys.exit(1)

    driver.quit()

main()
