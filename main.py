import requests
import selectorlib
import smtplib, ssl
import time
import sqlite3

URL = "https://programmer100.pythonanywhere.com/tours/"

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}


class Event:

    def scrap(self, url):  # to get the source code of the webpage
        response = requests.get(url)
        source = response.text
        return source

    def extract(self, source):
        extractor = selectorlib.Extractor.from_yaml_file("extract.yaml")  # to extract the needed data from source code
        value = extractor.extract(source)['tours']
        return value


class Database:
    def __init__(self, database_path):
        self.connection = sqlite3.connect(database_path)

    def read(self, extracted):  # to print out the data to use in emailing purpose only....
        row = extracted.split(",")
        row = [item.strip() for item in row]
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM events WHERE band_name=? AND city=? AND date=?", row)
        print(row)
        return row

    def store(self, extracted):  # to store the data to a file to keep it for later use while emailing
        row = extracted.split(",")
        row = [item.strip() for item in row]
        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO events VALUES(?,?,?)", row)
        self.connection.commit()


class Email:
    def send(self, message):
        host = "smtp.gmail.com"
        port = 465

        username = 'sonichimman@gmail.com'
        password = "pctd tvvc tbzb vnay"

        recivers_id = "pperter248@gmail.com"
        context = ssl.create_default_context()

        with smtplib.SMTP_SSL(host, port, context=context) as server:
            server.login(username, password)
            server.sendmail(username, recivers_id, message)

        print("message was sent successfully")


try:

    if __name__ == "__main__":
        while True:
            event = Event()
            scraped = event.scrap(URL)
            extracted = event.extract(scraped)
            print(extracted)

            if extracted != "No upcoming tours":
                database = Database(database_path="data.db")
                row = database.read(extracted)
                if extracted not in row:
                    database.store(extracted)
                    email = Email()
                    email.send(message="There is a new event uploaded on the site")

            time.sleep(1)
except KeyboardInterrupt:
    print("you stopped the Event scrapper")
    quit("bye bye!")
