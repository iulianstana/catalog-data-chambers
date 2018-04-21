
import time
import csv
import datetime
from pytz import utc, timezone
from pymongo import MongoClient

HOST = 'localhost'
PORT = '27017'


MONTHS = ['ian', 'feb', 'mart', 'apr', 'mai', 'iun', 'iul', 'aug', 'sept', 'oct', 'nov', 'dec']

POLITICIAN_NAME = 'name'
TEAMS_FIELD = 'formatiune'
LEGISLATION_FIELD = 'legislatie'

def get_politicians_names(politicians_collection):
    politicians = set()

    for politician_entry in politicians_collection.find({}):
        politicians.add(politician_entry['POLITICIAN_NAME'])

    return politicians


def get_month_number(month):
    try:
        return MONTHS.index(month) + 1
    except ValueError:
        return None

def parse_date_format(date_format):
    # Get month and year from data

    date_identifiers = ['până în', 'din']
    for identifier in date_identifiers:
        if identifier in date_format:
            date_format_shorted = date_format[date_format.index(identifier) + len(identifier):].strip()
    print(date_format_shorted)
    print(date_format_shorted.split(' '))
    month, year = [item.strip() for item in date_format_shorted.split(' ')[-2:]]

    # Remove dot from month, if it has
    if '.' in month:
        month = month[:-1]

    date_type = 0 if date_identifiers[0] in date_format else 1

    return date_type, year, get_month_number(month)


def get_legislation_end_date(legislation):
    now = datetime.datetime.now()
    if legislation + 4 > now.year:
        to_year, to_month = '-', '-'
    else:
        to_year, to_month = legislation + 4, 1

def parse_political_teams(political_doc, politician_name, aggregated_data):
    legislation = political_doc[LEGISLATION_FIELD]
    constituency = political_doc['circu']
    last_timestamp = datetime.datetime(legislation, 1, 1, tzinfo=timezone.utc)

    for formation in political_doc['formation'].keys():
        political_formation_entries = political_doc['formations'][formation]
        for formation_period in political_formation_entries:
            if len(formation_period) == 2:
                # If we have a start date and an end date
                _, from_year, from_month = parse_date_format(formation_period[0])
                _, to_year, to_month = parse_date_format(formation_period[1])
            elif len(formation_period) == 1:
                # If we have a start date or an end date
                type, year, month = parse_date_format(formation_period[0])
                if type == 0:
                    from_year, from_month = legislation, 1
                    to_year, to_month = year, month
                else:
                    from_year, from_month = year, month
                    to_year, to_month = get_legislation_end_date(legislation)
            else:
                # If we have only one political formation the entire legislation interval
                from_year, from_month = legislation, 1
                to_year, to_month = get_legislation_end_date(legislation)

            aggregated_data.append((politician_name,
                                    from_year,
                                    from_month,
                                    formation,
                                    constituency,
                                    to_year,
                                    to_month
                                    ))


def aggregate_legislations_for_politician(politicians_collection, politician_name):
    aggregated_data = []

    for legislation_doc in politicians_collection.find({"name": politician_name}):
        parse_political_teams(legislation_doc, politician_name, aggregated_data)

#     Sort data

def parse(db):
    collection = db['collection_default']
    politicians_names = get_politicians_names(collection)
    data = {politician_name: aggregate_legislations_for_politician(collection, politician_name) for politician_name in politicians_names}


def write_csv_results(filename, data):
    with open(filename, 'w') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_NONNUMERIC)
        writer.writerow(["Nume politician", "an_inceput", "luna_inceput", "partid", "circumscriptie", "an_sfarsit", "luna_sfarsit"])
        for politician_name in data:
            for political_period in data[politician_name]:
                writer.writerow(political_period)


if __name__ == '__main__':

    # client = MongoClient('localhost', 27017)
    # db = client['catalog']
    # data = parse(db)

    # write_csv_results("test.csv", {"ana": [("1213", "2121", "partid", "mures"), ("1213", "2121", "partid", "mures")]})
