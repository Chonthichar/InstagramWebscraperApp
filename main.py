import json
import re
import pandas as pd
import asyncio
import time
import requests
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.floatlayout import FloatLayout
from kivymd import app
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRectangleFlatButton, MDFloatingActionButton, MDFlatButton, MDRaisedButton
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.textfield import MDTextField
from selenium.webdriver.chrome.service import Service
from seleniumwire import webdriver
from datetime import datetime
from kivy.uix.label import Label
from kivymd.uix.datatables import MDDataTable
from kivy.uix.screenmanager import Screen
from kivy.metrics import dp
import subprocess
from kivymd.uix.spinner import MDSpinner
from kivy.graphics import Color, Rectangle
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService


class Demo(FloatLayout):
    pass


class CustomOverFlowMenu(MDDropdownMenu):
    # In this class, you can set custom properties for the overflow menu.
    pass


# KivyMD GUI
username_helper = """
MDTextField:
    orientation: "vertical"
    # font_size: 13
    font_style: "H6"
    md_bg_color: 1, 1, 1, 1
    hint_text: "Enter the instagram's username"
    # helper_text: "Open the calender to select the date"
    helper_text_mode: "on_focus"
    icon_right: "username"
    icon_right_color: app.theme_cls.primary_color
    pos_hint: {'center_x':0.5,'center_y': 0.5}
    max_length_text_color: 0, 1, 0, 1
    # mode: "fill"
    fill_color: 0,0,0,4
    size_hint_x: None
    width: 400
    # hint_text: ""
    # mode: "rectangle"
"""

search_field = """
MDTextField:
    orientation: "vertical"
    # font_size: 13
    font_style: "H6"
    hint_text: "Enter hastags"
    # helper_text: "Open the calender to select the date"
    helper_text_mode: "on_focus"
    icon_right: "username"
    icon_right_color: app.theme_cls.primary_color
    pos_hint: {'center_x':0.5,'center_y': 0.5}
    max_length_text_color: 0, 1, 0, 1
    size_hint_x: None
    width: 400
    # mode: "fill"
    fill_color: 0,0,0,4
    # hint_text: ""
    # mode: "rectangle"
"""

date_helper_start = """
MDTextField:
    hint_text: "Enter your date here"
    font_size: 20
    # helper_text: "or click on forgot username"
    helper_text_mode: "on_focus"
    icon_right: "calendar"
    icon_right_color: app.theme_cls.primary_color
    pos_hint: {'center_x':0.5, 'center_y': 0.5}
    size_hint_x: None
    width: 400
    hint_text: "Start Date"
    mode: "fill"
    fill_color: 0,0,0,4
"""

date_helper_end = """
MDTextField:
    hint_text: "Enter your date here"
    font_size: 20
    # helper_text: "or click on forgot username"
    helper_text_mode: "on_focus"
    icon_right: "calendar"
    icon_right_color: app.theme_cls.primary_color
    pos_hint: {'center_x':0.5, 'center_y': 0.5}
    size_hint_x: None
    # spacing: 50
    width: 400
    hint_text: "End Date"
    mode: "fill"
    fill_color: 0,0,0,4
    padding: "50dp"
"""

start_button = '''
#:import MagicBehavior kivymd.uix.behaviors.MagicBehavior


<MagicButton@MagicBehavior+MDRectangleFlatButton>
FloatLayout:

    MagicButton:
        text: "WOBBLE EFFECT"
        on_release: self.wobble()
        pos_hint: {"center_x": .5, "center_y": .3}
        on_release: self.scrape_data
    '''

KV = '''
#:import CustomOverFlowMenu __main__.CustomOverFlowMenu
#:import Demo __main__.Demo
#: import get_color_from_hex kivy.utils.get_color_from_hex

BoxLayout:
    orientation: "vertical"
    specific_text_color: 0, 0, 0, 1

    MDTopAppBar:
        title: "Instagram Scraper"
        font_size: 20
        bold: True
        md_bg_color: 1, 1, 1, 1
        specific_text_color: 0, 0, 0, 1
        elevation: 0.1
        left_action_items: [['instagram', lambda x: x]]
        use_overflow: True
        overflow_cls: CustomOverFlowMenu()

    MDLabel:
        font_size: 15
        center_x: 1
        center_y: 1


    MDLabel:
        text: "Scrape and download Instagram posts, profiles, hashtags, photos, comments. Download your data as CSV."
        padding: 100
        pos_hint: {"center_x": 0.5, "center_y": 0.5}
        font_size: 20

    BoxLayout:
        orientation: "horizontal"
        size_hint_y: None
        height: "48dp"
        spacing: "16dp"
        padding: "16dp"
'''


class InstagramScraperApp(MDApp):
    username = StringProperty()
    start_date = StringProperty()
    end_date = StringProperty()

    def build(self):
        self.theme_cls.primary_palette = 'BlueGray'
        screen = Screen()

        self.start_date_input = Builder.load_string(date_helper_start)
        self.end_date_input = Builder.load_string(date_helper_end)
        self.username_input = Builder.load_string(username_helper)
        self.search_field = Builder.load_string(search_field)

        self.data_label = Label(
            text='save and see the change',
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )

        self.start_button = MDRaisedButton(
            text='Save and Start',
            icon="archive-arrow-down",
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            size_hint_y=None,
            height="16dp",
            font_size="22",
            width=dp(500),
            padding=dp(10),
            top=dp(400),
            elevation=1,
            # height=dp(200),
            on_release=self.scrape_data
        )

        self.output_label = Label(
            text='',
            # color='#000000',
            font_size='20',
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
        )

        self.execution_time_label = Label(
            text='',
            color='#000000',
            font_size='20',
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
        )

        # Set the background color directly using the canvas.before property
        with self.execution_time_label.canvas.before:
            Color(0.9, 0.9, 0.9, 1)  # Replace these values with the desired color (RGBA format)

        self.spinner = MDSpinner(size_hint=(None, None),
                                 active=False)

        layout = MDBoxLayout(orientation='vertical')

        self.kv = Builder.load_string(KV)
        layout.add_widget(self.kv)

        layout.add_widget(self.username_input)
        layout.add_widget(self.search_field)
        layout.add_widget(self.start_date_input)
        layout.add_widget(self.end_date_input)
        layout.add_widget(self.data_label)
        layout.add_widget(self.start_button)
        layout.add_widget(self.execution_time_label)
        screen.add_widget(layout)

        return screen

    def scrape_data(self, *args):
        username = self.username_input.text.strip()
        start_date_str = self.start_date_input.text.strip()
        end_date_str = self.end_date_input.text.strip()
        search_hashtags = self.search_field.text.strip()

        # Launch the Chrome driver instance with the proxy
        # chromedriver_path = r"path of Chromedriver-win32/chromedriver-win32/chromedriver.exe"
        # service = Service(chromedriver_path)
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')  # Hide GUI

        # driver = webdriver.Chrome(options=chrome_options, service=service)
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),
                                  options=chrome_options)

        # Define the date range (start and end dates)
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d")

        # Open the Instagram user profile page
        driver.get(f'https://www.instagram.com/{username}')
        time.sleep(10)

        # Get the page source
        page_source = driver.page_source

        # Search for the user ID, username, name, and categories using regular expressions
        user_id_match = re.search(r'"profilePage_(\d+)"', page_source)
        username_match = re.search(r'"username":"([A-Za-z0-9_]+)"', page_source)

        if user_id_match and username_match:
            user_id = user_id_match.group(1)
            username = username_match.group(1)
            print(f"User ID for {username}: {user_id}")
        else:
            print("Failed to retrieve user ID or username")
            driver.quit()
            exit()

        # Quit the driver instance
        driver.quit()

        # Define the variables for scraping
        links = []
        total_interactions = [0]  # Use a mutable object to store the total interactions
        has_next_page = True
        end_cursor = ''

        # Create a session for API requests
        session = requests.Session()
        session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })

        # show the spinner while code ececuted
        self.spinner.active = True

        # Calculate the execution time
        start_time = time.time()  # To record the start time

        # Get a list of hastags from the comma seperated input
        search_hashtags_list = [tag.strip() for tag in search_hashtags.split(",")]

        # Continue scraping until there are no more pages
        while has_next_page:
            # Construct the API query URL
            api_url = f'https://www.instagram.com/graphql/query/?query_hash=42323d64886122307be10013ad2dcc44&variables={{"id":"{user_id}","first":50,"after":"{end_cursor}"}}'

            # Make the API request
            response = session.get(api_url)
            parsed_json = response.json()

            if 'data' in parsed_json and 'user' in parsed_json['data']:
                user_data = parsed_json['data']['user']
                total_posts = user_data['edge_owner_to_timeline_media']['count']

                if 'edge_owner_to_timeline_media' in user_data:
                    has_next_page = user_data['edge_owner_to_timeline_media']['page_info']['has_next_page']
                    end_cursor = user_data['edge_owner_to_timeline_media']['page_info']['end_cursor']

                    async def process_post(each, links, total_interactions):
                        taken_at_timestamp = each['node']['taken_at_timestamp']
                        postdate = time.strftime('%Y-%m-%d', time.localtime(taken_at_timestamp))
                        post_datetime = datetime.strptime(postdate, "%Y-%m-%d")
                        # Filter posts based on the date range and hashtags
                        if start_date <= post_datetime <= end_date:
                            link = 'https://www.instagram.com/p/' + each['node']['shortcode'] + '/'
                            caption_edges = each['node']['edge_media_to_caption']['edges']
                            if caption_edges:
                                posttext = caption_edges[0]['node']['text'].replace('\n', '')
                                caption_hashtags = re.findall(r'#(\w+)', posttext)
                                hashtags_string = ', '.join(caption_hashtags)
                                # Check if any of the entered hashtags are present in the post
                                if not search_hashtags_list or any(
                                        hashtag.lower() in hashtags_string.lower() for hashtag in search_hashtags_list):
                                    comments = each['node']['edge_media_to_comment']['count']
                                    likes = each['node']['edge_media_preview_like']['count']
                                    postimage = each['node']['thumbnail_src']
                                    isvideo = each['node']['is_video']
                                    postdate = time.strftime('%Y %b %d %H:%M:%S', time.localtime(taken_at_timestamp))
                                    interactions = likes + comments
                                    total_interactions[0] += interactions
                                    links.append([
                                        postdate,
                                        link,
                                        posttext,
                                        comments,
                                        likes,
                                        postimage,
                                        isvideo,
                                        interactions,
                                        hashtags_string
                                    ])

                    # Process posts asynchronously
                    event_loop = asyncio.get_event_loop()
                    tasks = [event_loop.create_task(process_post(each, links, total_interactions)) for each in
                             user_data['edge_owner_to_timeline_media']['edges']]
                    event_loop.run_until_complete(asyncio.wait(tasks))

        # Get the number of users the profile is following
        following_count = 0
        follower_count = 0
        response = session.get(f'https://instagram.com/{username}/?__a=1&__d=dis')
        if response.status_code == 200:
            try:
                data = response.json()
                user_data = data['graphql']['user']
                Name = user_data['full_name']
                category = user_data['category_name']
                following_count = user_data['edge_follow']['count']
                follower_count = user_data['edge_followed_by']['count']
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON response: {e}")
                print(f"Response content: {response.content}")

        # Create DataFrame
        table = pd.DataFrame(
            links,
            columns=[
                'Post Date',
                'Link',
                'Posts',
                'Number of comments',
                'Number of likes',
                'Image Link',
                'Video(True or False)',
                'Interactions',
                'Hashtags'
            ]
        )
        table['Username'] = username
        table['Name'] = Name
        table['Category'] = category
        table['Total Posts'] = total_posts
        table['Followers'] = follower_count
        table['Following'] = following_count

        table.to_csv("output_dataFast.csv")

        # Open the CSV file with the default application
        subprocess.run(["start", "output_dataFast.csv"], shell=True)

        # Update the data_label text
        self.data_label.text = f"Scraped data for {username}. Total interactions: {total_interactions[0]}"

        # Quit the session
        session.close()

        # Hide the spinner when the code finished executing
        self.spinner.active = False

        execution_time = time.time() - start_time
        formatted_time = f"{execution_time: .2f} seconds"

        # Update the data label text
        self.data_label.text = f"Scrape data for {username}."

        # Update the excecuted time label
        self.execution_time_label.text = f"Execution Time: {formatted_time}"

        # Reset the text of the input fields
        self.username_input.text = ""
        self.search_field.text = ""

    def on_start(self):
        # Set initial start and end dates
        self.start_date = datetime.now().strftime("%Y-%m-%d")
        self.end_date = datetime.now().strftime("%Y-%m-%d")

        # Update the start_date_input and end_date_input text
        self.start_date_input.text = self.start_date
        self.end_date_input.text = self.end_date

        # Reset the text of input field
        self.username_input.text = ""
        self.username_input.text = ""


if __name__ == "__main__":
    InstagramScraperApp().run()
