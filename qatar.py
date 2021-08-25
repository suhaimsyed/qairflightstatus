import csv
import json
import ssl
from collections import Counter

from datetime import datetime, timedelta
from pip._vendor import requests

ssl.OPENSSL_VERSION

header = {
    'Content-Type': 'application/json',
    'Host': 'qoreservices.qatarairways.com'
}


class my_dictionary(dict):

    # __init__ function
    def __init__(self):
        self = dict()

        # Function to add key:value

    def add(self, key, value):
        self[key] = value


dict = my_dictionary()


def callToApi(departureStation, arrivalStation, date):
    data = {
        'departureStation': departureStation,
        'arrivalStation': arrivalStation,
        'scheduledDate': date.strftime('%Y-%m-%d'),
        'appLocale': 'en'
    }
    result = requests.post(
        'https://qoreservices.qatarairways.com/fltstatus-services/flight/getStatus',
        headers=header, verify=False, data=json.dumps(data))
    result_1 = json.loads(result.content)
    if 'flights' in result_1:
        for flight in result_1['flights']:
            if flight['flightStatus'] == 'SCHEDULED' \
                    or flight['flightStatus'] == 'ARRIVED' \
                    or flight['flightStatus'] == 'DELAYED':
                my_dictionary.add(dict, flight['departureDateScheduled'], 'SCHEDULED')
            elif flight['flightStatus'] == 'CANCELLED':
                my_dictionary.add(dict, flight['departureDateScheduled'], 'CANCELLED')


def invokeAndGenerateReportForEachFlight(departureStation, arrivalStation):
    # T-2
    date = datetime.today() - timedelta(2);
    callToApi(departureStation, arrivalStation, date)
    # T-1
    date = datetime.today() - timedelta(1);
    callToApi(departureStation, arrivalStation, date)
    # T-0
    date = datetime.today()
    callToApi(departureStation, arrivalStation, date)
    # T+1
    date = datetime.today() + timedelta(1)
    callToApi(departureStation, arrivalStation, date)
    # T+2
    date = datetime.today() + timedelta(2)
    callToApi(departureStation, arrivalStation, date)
    # T+3
    date = datetime.today() + timedelta(3)
    callToApi(departureStation, arrivalStation, date)
    # T+4
    date = datetime.today() + timedelta(4)
    callToApi(departureStation, arrivalStation, date)
    # T+5
    date = datetime.today() + timedelta(5)
    callToApi(departureStation, arrivalStation, date)
    res = Counter(dict.values())
    field_names = ['date', 'status']
    # Open our existing CSV file in append mode
    # Create a file object for this file
    filename = departureStation + '_' + arrivalStation + '.csv'
    with open(filename, 'w+') as csv_file:
        reader = csv.reader(csv_file, delimiter=",")
        for i in reader:
            if i[0] in dict:
                del dict[i[0]]
        writer = csv.writer(csv_file)
        for key, value in dict.items():
            writer.writerow([key, value])


dict.clear()
departureStation = 'DOH'
arrivalStation = 'FRA'
invokeAndGenerateReportForEachFlight(departureStation, arrivalStation)
