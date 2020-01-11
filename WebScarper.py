from bs4 import BeautifulSoup
import requests
from datetime import date
import datetime


class OrbitalLaunch:

    def finder(self, url):
        website_url = requests.get(url).text
        soup = BeautifulSoup(website_url, 'lxml')
        wiki_table = soup.find('table', {'class': 'wikitable'})
        date_found = ''

        rows = wiki_table.find_all('tr')
        map = {}
        final_list = {}
        status = ["Successful", "Operational", "En route"]

        for row in rows[2:]:
            cols = row.findAll(["td"])

            if len(cols) > 2:
                # print(cols[0].getText())
                if len(cols) == 5:
                    if cols[0].getText().split('[')[0].split(':')[0][-1].isdigit():
                        date_found = cols[0].getText().split('[')[0].split(':')[0][:-2]
                    else:
                        date_found = cols[0].getText().split('[')[0].split(':')[0]
                    format = '%d %B'
                    date_found = date_found.split('(')[0].rstrip()
                    date_found = datetime.datetime.strptime(date_found, format).replace(year=2019)
                    date_found = str(date_found).split()[0] + 'T' + str(date_found).split()[1] + "+00:00"
                    map[date_found] = 0
                else:
                    if cols[5].getText().rstrip() in status:
                        value = map[date_found]
                        value = value + 1
                        map[date_found] = value

        sdate = date(2019, 1, 1)
        edate = date(2019, 12, 31)

        delta = edate - sdate

        for i in range(delta.days + 1):
            day = sdate + datetime.timedelta(days=i)
            if day.strftime("%Y-%m-%dT%H:%M:%S+00:00") in map.keys():
                print(day.strftime("%Y-%m-%dT%H:%M:%S+00:00"))
                value = map[day.strftime("%Y-%m-%dT%H:%M:%S+00:00")]
                final_list[day.strftime("%Y-%m-%dT%H:%M:%S+00:00")] = value
            else:
                final_list[day.strftime("%Y-%m-%dT%H:%M:%S+00:00")] = 0

        self.send_results(final_list)

    def send_results(self,map):
         file = open('output.csv', 'w')
         file.write("date,value\n")
         for key in map.keys():
           file.write(str(key) + "," + str(map[key]) + "\n")


OrbitalLaunch().finder("https://en.wikipedia.org/wiki/2019_in_spaceflight#Orbital_launches")
