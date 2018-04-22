
import time
import csv
import datetime
from pytz import utc, timezone
from pymongo import MongoClient

HOST = 'localhost'
PORT = '28000'


MONTHS = ['ian', 'feb', 'mar', 'apr', 'mai', 'iun', 'iul', 'aug', 'sep', 'oct', 'noi', 'dec']

POLITICIAN_NAME = 'name'
FORMATIONS_FIELD = 'formations'
LEGISLATION_FIELD = 'leg'

ELECTION_DATES = {
    1990: [(1990, 5), (1992, 9)],
    1992: [(1992, 9), (1996, 11)],
    1996: [(1996, 11), (2000, 11)],
    2000: [(2000, 11), (2004, 11)],
    2004: [(2004, 11), (2008, 11)],
    2008: [(2008, 11), (2012, 11)],
    2012: [(2012, 12), (2016, 12)],
    2016: [(2016, 12), (2018, 12)] # hardcoded cause no better ideea
}


def get_politicians_names(politicians_collection):
    politicians = set()

    for politician_entry in politicians_collection.find({}):
        if politician_entry.get(POLITICIAN_NAME):
            politicians.add(politician_entry[POLITICIAN_NAME])

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

    month, year = [item.strip() for item in date_format_shorted.split(' ')[-2:]]

    # Remove dot from month, if it has
    if '.' in month:
        month = month[:-1]

    date_type = 0 if date_identifiers[0] in date_format else 1

    return date_type, year, get_month_number(month)


def get_legislation_date(legislation, start=False):
    if start:
        year, month = ELECTION_DATES[int(legislation)][0]
    else:
        year, month = ELECTION_DATES[int(legislation)][1]

    return year, month


def parse_political_teams(political_doc, politician_name, aggregated_data):
    legislation = political_doc[LEGISLATION_FIELD]
    # constituency = political_doc['circu']

    for formation in political_doc[FORMATIONS_FIELD].keys():
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
                    from_year, from_month = get_legislation_date(legislation, start=True)
                    to_year, to_month = year, month
                else:
                    from_year, from_month = year, month
                    to_year, to_month = get_legislation_date(legislation)
            else:
                # If we have only one political formation the entire legislation interval
                from_year, from_month = get_legislation_date(legislation, start=True)
                to_year, to_month = get_legislation_date(legislation)

            aggregated_data.append((politician_name,
                                    int(from_year),
                                    int(from_month),
                                    formation,
                                    '',
                                    int(to_year),
                                    int(to_month)
                                    ))


def aggregate_legislations_for_politician(politicians_collection, politician_name):
    aggregated_data = []

    for legislation_doc in politicians_collection.find({"name": politician_name}):
        if legislation_doc.get(FORMATIONS_FIELD):
            parse_political_teams(legislation_doc, politician_name, aggregated_data)

    # Sort data
    aggregated_data = sorted(aggregated_data, key=lambda agg_data: datetime.datetime(year=agg_data[1], month=agg_data[2], day=1))

    return aggregated_data


def parse(db):
    collection = db['default_collection']
    politicians_names = get_politicians_names(collection)

    return {politician_name: aggregate_legislations_for_politician(collection, politician_name) for politician_name in politicians_names}


def write_csv_results(filename, data):
    with open(filename, 'w') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_NONNUMERIC)
        writer.writerow(["Nume politician", "an_inceput", "luna_inceput", "partid", "circumscriptie", "an_sfarsit", "luna_sfarsit"])
        for politician_name in data:
            for political_period in data[politician_name]:
                writer.writerow(political_period)


def save_to_visualisation_db(db, data):
    collection = db['visualise_data']
    for politician in data.keys():
        doc = {'name': politician, 'activity': []}
        for activity in data[politician]:
            doc['activity'].append({'since':
                                        {'year': activity[1],
                                         'month': activity[2]},
                                    'until':
                                        {'year': activity[5],
                                         'month': activity[6]},
                                    'formation': activity[3],
                                    })
        collection.insert_one(doc)


if __name__ == '__main__':

    client = MongoClient(HOST, int(PORT))
    db = client['catalog']
    data = parse(db)

    write_csv_results("test.csv", data)
    save_to_visualisation_db(db, data)
