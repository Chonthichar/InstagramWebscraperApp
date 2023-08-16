# InstagramWebscraper

This KivyMD Application allows user to scrape specific data from Instagram profiles with in a specific date range and save it to a CSV file and, optionally, containing certain hashtags.
The codebase is divided into two files:
1. main.py (Extract Data without using Proxy)
2. main_proxy.py (Extract Data using Proxy)

### Prerequisites:
1. Python environment.
2. Necessary libraries installed(e.g., Kivy, requests, pandas).
3. Ensure Chrome driver is available and its path is correctly set in the code.

## main.py (Extract Data without using Proxy)

### Code Structure:
#### 1. Imports:
Make sure you have all the required packages installed. THe code assumes you've imported listed libary including
Kivy,KivyMD, Web scraping tools like selenium and relevant libraries.

#### 2. InstagramScraperApp:
"InstagramScraperApp" is a main application class that inherits from "MDApp", a part of the kivy framework, Utilizes Kivy and MDAppfor a user friendly interface.

- Attributes:
    - 'username': Input the Instagram username to scrape.
    - 'search_hashtags': Input the hashtags of that user to scrape post base on that hashtags.
    - 'start_date': The start date for scraping.
    - 'end_date': The end date for scraping.
- Methods:
    - 'build()': Set up the main GUI for an application
    - 'scrape_data(*args)': Responsible for the actual scraping of Instagram data.
    - 'on_start()': Initializes certain values when the app starts.

#### 3. Inside the 'build()' method, various UI elements are defined:
- Input Fields:
    - 'username_input': Input field for entering the Instagram username.
    - 'start_date_input' and 'end_date_input': Date input fields.
    - 'search_filed': Input field for search hashtags.
- Button and Labels:
    - 'start_button': Button to start scraping process.
    - 'date_label': Label to display messages to the user.
    - 'execution_time_label': Label to display how long the scraping took.
- Others:
    -'spinner': KivyMD loading spinner that shows while scraping is in progress.


#### 4. Scraping Logic:
Inside the 'scrape_data()' method

4.1 The application sets up a Chrome WebDriver instance.
Users must have ChromeDriver installed on their local machine. After installation, they need to point the directory path of ChromDriver in the code. Two option are available for this confoguration:
       -  Local directory path  Chromedriver_path = r"C:\Users\bruker1\Downloads\chromedriver_win32\chromedriver.exe"
       -  Remote Selenium Chrome Driver: driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),
                                  options=chrome_options,
                                  seleniumwire_options=options)
                                  
4.2 Fetch the instagram page of the provide username.
This involves using the WebDriver instance to navigate to the specific Instagram page URL associated with the username
provided by the user. The code accomplishes by appending the username to the base Instagram profile URL
(https://www.instagram.com/{username}).

4.3 Using regular expression to extract user data:
- Once input the user's Instagram username. ChromeDriver will redirected to user's Instagram page, the application reads the page source which is essentially the raw HTML content of the page.
- In the code, regex is employed to search and extract specific pieces of information like user ID, username, name and categories from the page source. These are defined to match specific formats or string in the Instagram's HTML structure.

4.4 Making Additional API Requests to Get Post Details:
- The primary profile page doesn't contain all the data needed, and to be able to scrape more than 50 posts.\
So the program make additional requests to Instagram's GraphQL API. This API provides a structure way to retrieve details data about each post, including others data.

4.5 Processing Posts Asynchronously:
Instead of processing each post one after the other (synchronously), the program processes multiple posts simultaneously (asynchronously).
This approach speed up data extraction, especially when dealing with profiles that have many posts. Using Python's "asyncio" library, the program can send out multiple requests or process multiple set of data without wating for one to complete before starting the next.

4.6 Storing Data in a Pandas DataFrame and Writing to a CSV File:
- After data is extracted, it's organized and stored in a Pandas DataFrame which provide a structured way to store tabular data, making it easy to analyze, and sort data.
- After populating the DataFrame, the program writes this data to a CSV(Comma-Separated Values) file.

### 5. Starting the Application:
The application is initialized and run through the main entry point:
if __name__ == "__main__":
    InstagramScraperApp().run()


### How to use:
1. Make sure you have installed all the required packages.
2. Input the instagram username you want to scrape in the "username_input" field.
3. Select the desired "start_date" and "end_date"
4. (Optional) Enter any specific hashtags you want to filter by in the "search_field".
5. Click the "start_button" to begin the scraping process.
6. Once the scraping is complete, a CSV file will be automatically opened containing the scraped data.

### Important Notes:
1. Instagram endpoint query: Initially, we used the endpoint 'https://instagram.com/{username}/?__a=1&__d=dis' to fetch data.
However, the JSON response from this query only allows scraping of 12 posts. To overcome this limitation, we switched to the Instagram API endpoint, which lets us specify up to 50 posts per page.
We then iteratively made request to the API, continuing our scraping until we covered all available pages for our desired date range.
2. Extraction speed: The speed at which data is extracted largely depends on the internet traffic and concurrency at the given time.
3. Data Collection: To gather comprehensive data, we utilized another Instagram query. This helps us populate the table with the following fields:
    - 'Username': which holds the username.
    - 'Name': for the account name.
    - 'Category': to specify the category of the account.
    - 'Total Posts': which provide the total number of posts.
    - 'Follower': indicating the follower count.
    - 'Following' showing the count of accounts the user is following.
4. Instagram Web Structure Dependency: The code primarily relies on Instagram's HTML web structure and query endpoints. If the web structure changes, the code may malfunction. For instance: It may fail to extract the Instagram user ID.
5. Large Data Set: The code might experience extended processing times when scraping data from over 10,000 posts, or it could potentially malfunction toward the end.
6. Proxy usage: The code is capable of scraping data without utilizing a proxy. However, there maybe instances when scraping is disrupted because Instagram detects and tracks your activity.

### Troubleshooting
1. Failed to Scrape User ID: Ensure Instagram's structure hasn't been updated. If it has the code might need an update.
2. Slowed Performance with large data sets: Consider scraping data in smaller batches or optimizing the code further for better performance.
3. Consider switching to a different WIFI network or using a VPN if you encounter the error : Please wait a few minutes before you try again' or 'Failed to retrieve user ID or username'.


## main_proxy.py (Extract Data using Proxy)

### Overview
'main_proxy.py' allows for the extraction of Instagram data with the added benefit of using proxies. The implementation is much the same as
'main.py', but with proxy support for better privacy and to counter potential blocking by Instagram.

### Getting start
1. You can simply update the proxy settings in the options dictionary.
2. Ensure your proxy provider is compatible set the necessary configurations.

### Important Notes
1. Performance: Using a proxy might slow down the execution time compared to 'main.py'.
2. Proxy implementation: The proxy is integrated at three key points where requests are made to Instagram.
3. Rotating Proxy: It is recommend to use rotating proxies to ensure Instagram doesn't detect and block your activities.
