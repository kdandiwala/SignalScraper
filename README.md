# SignalScraper
Download the requested signals from www.sigidwiki.com based on their category or frequency. 

## Setting up Selenium

Setting up Selenium requires two components: the Selenium Python package and the browser driver (Chromedriver in this case).

### Selenium Package

To download the Selenium package, execute the pip command in your terminal:

```shell Tab A
pip3 install selenium 
```

### Selenium Drivers

This script requires a Chromedriver. Verify the version of your Chrome installed by clicking the 3 dots on the top right of Chrome, clicking Settings, and navigating to About Chrome. Take a note of the version number. 

Download the Chromedriver for your specific OS and Chrome version from [here](https://chromedriver.chromium.org/downloads).

Once you download the executable appropriate for your operating system, extract it and place it in a folder. Take a note of the folder path and insert the path into the line shown below (line 23):

```python
driver = webdriver.Chrome('INSERT CHROMEDRIVER PATH HERE',  options=chrome_options)
```

If the error `chromedriver cannot be opened because the developer cannot be verified` is recieved for MacOS:
1. Open the terminal
2. Navigate to path where your chromedriver file is located
3. Execute ```xattr -d com.apple.quarantine chromedriver```

### Download Folder

Note the path of the desired download location for the signals and insert it into the line shown below (line 13):

```python
downloads = Path("INSERT DOWNLOAD PATH HERE")
```
