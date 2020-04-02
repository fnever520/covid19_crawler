from selenium import webdriver
from time import sleep
import re
from datetime import datetime
import smtplib

class Coronavirus():
    def __init__(self):
        self.driver = webdriver.Chrome()

    def get_data(self):
        country = "Malaysia"
        try:
            country_contains = "contains(., '%s')" %country
            
            self.driver.get('https://www.worldometers.info/coronavirus/')
            table = self.driver.find_element_by_xpath(
                '//*[@id="main_table_countries_today"]/tbody[1]')
            country_element = table.find_element_by_xpath(
                '//td[%s]' %country_contains)
            row = country_element.find_element_by_xpath("./..")
            data = row.text.split(" ")
            total_cases = data[1]
            new_cases = data[2]
            total_deaths = data[3]
            new_deaths = data[4]
            active_cases = data[5]
            total_recovered = data[6]
            serious_critical = data[7]

            print("Country:" + country_element.text)
            print("Total cases:" + total_cases)
            print("New Cases:" + new_cases)
            print("Total Deaths:" + total_deaths)
            print("New Deaths:" + new_deaths)
            print("Active Cases:" + active_cases)
            print("Total Recovered:" + total_recovered)
            print("Serious Critical:" + serious_critical)

            send_mail(country_element.text, total_cases, new_cases, total_deaths, new_deaths, active_cases, total_recovered, serious_critical)

            self.driver.close()

        except Exception as e:
            print(e)
            self.driver.quit()

def send_mail(country_element, total_cases, new_cases, total_deaths, new_deaths, active_cases, total_recovered, serious_critical):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    server.login('fnever520@gmail.com', 'srytfmkcjaxekjnw')

    subject = 'Coronavirus stats in your country today'

    body = 'News today in ' + country_element + '\
        \nThere is new data on covid-19: \
        \nTotal cases: ' + total_cases + '\
        \nNew cases: ' + new_cases + '\
        \nTotal Deaths: ' + total_deaths +'\
        \nNew Deaths: ' + new_deaths + '\
        \nActive Cases: ' + active_cases + '\
        \nTotal Recovered: ' + total_recovered + '\
        \nSerious Critical: ' + serious_critical + '\
        \nCheck out this link: https://www.worldometers.info/coronavirus/'

    
    msg = f"Subject: {subject}\n\n{body}"

    server.sendmail(
        'Covid-19',
        'fnever520@gmail.com',
        msg
    )

    print('The email has been sent!')

    server.quit()

bot = Coronavirus()
bot.get_data()
