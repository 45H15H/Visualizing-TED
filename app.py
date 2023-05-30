import streamlit as st

import time

from bs4 import BeautifulSoup

from selenium import webdriver

from selenium.webdriver.common.by import By

from wordcloud import WordCloud, STOPWORDS

import matplotlib.pyplot as plt

from PIL import Image
import numpy as np

options = webdriver.EdgeOptions()
options.add_argument('--incognito')
options.add_argument('--headless')

driver = webdriver.Edge('msedgedriver.exe', options=options)

def make_transcript_file():
    driver.get("https://www.ted.com/talks/shannon_odell_what_s_the_smartest_age")

    # use xpath when same class or id is used for buttons. otherwise you will get invalidselectorexception error
    read_transcript_button = driver.find_element(By.XPATH, "/html/body/div[1]/div/main/div/div/div/div/div[2]/div[1]/div[4]/button")

    # click the button
    read_transcript_button.click()

    time.sleep(2)

    page_source = driver.page_source

    driver.close()

    soup = BeautifulSoup(page_source, 'html.parser')

    main = soup.find('div', class_ = "mb-10 w-full")

    transcripts = main.find('div', class_ = "w-full")

    transcripts_each = transcripts.find_all('div', class_ = "mb-6 w-full")

    # print(len(transcripts_each))

    speech_block = []
    for i in range(len(transcripts_each)):
        speech_block.append(transcripts_each[i].span.text)

    full_text = " ".join(speech_block)
    with open('transript_new.txt', 'w') as file:
        file.write(full_text)
        file.close()

    # read the file
    with open('transript_new.txt', 'r') as file:
        full_text = file.read()
        file.close()

    return full_text

    # print(speech_block)

# def make_binary_image():
#     image_file = Image.open("ted-logo-fb.png") # open colour image
#     thresh = 200
#     image_file = image_file.convert('L')
#     width, height = image_file.size
#     for x in range(width):
#         for y in range(height):
#             if image_file.getpixel((x, y)) < thresh:
#                 image_file.putpixel((x, y), 0)
#             else:
#                 image_file.putpixel((x, y), 255)


#     image_file.save('binary-logo.png')

text = make_transcript_file()

# discard = STOPWORDS

# cloud = WordCloud(background_color=(255, 255, 255), stopwords = discard, mask= customMask).generate(text)

st.text_area("Transcript", text, height=500)