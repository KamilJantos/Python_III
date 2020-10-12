import json
import xml.etree.ElementTree as etree
import sqlite3 as sqlite3
import sys


class JSONDataExtractor:
    def __init__(self, filepath):
        self.data = dict()
        with open(filepath, mode='r', encoding='utf-8') as f:
            self.data = json.load(f)

    @property
    def parsed_data(self):
        return self.data


class XMLDataExtractor:
    def __init__(self, filepath):
        self.tree = etree.parse(filepath)

    @property
    def parsed_data(self):
        return self.tree


class SQLDataExtractor:
    def __init__(self, filepath):
        try:
            con = sqlite3.connect(filepath)
            cursor = con.cursor()
            cursor.execute('SELECT * from genres')
            data = cursor.fetchall()
            print("Data from table: {}".format(data))
        except sqlite3.Error as error:
            print("Connection error: {}".format(error))
            sys.exit(1)
        finally:
            if con:
                con.close()
                print("The SQLite connection is closed")


def dataextraction_factory(filepath):
    if filepath.endswith('json'):
        extractor = JSONDataExtractor
    elif filepath.endswith('xml'):
        extractor = XMLDataExtractor
    elif filepath.endswith('db'):
        extractor = SQLDataExtractor
    else:
        raise ValueError('Cannot extract data from {}'.format(filepath))
    return extractor(filepath)


def extract_data_from(filepath):
    factory_obj = None
    try:
        factory_obj = dataextraction_factory(filepath)
    except ValueError as e:
        print(e)
    return factory_obj


def main():
    sqlite_factory = extract_data_from('data/chinook.db')
    print()

    json_factory = extract_data_from('movies.json')
    json_data = json_factory.parsed_data
    print(f'Found: {len(json_data)} movies')
    for movie in json_data:
        print(f"Title: {movie['title']}")
        year = movie['year']
        if year:
            print(f"Year: {year}")
        director = movie['director']
        if director:
            print(f"Director: {director}")
        genre = movie['genre']
        if genre:
            print(f"Genre: {genre}")
    print()

    xml_factory = extract_data_from('person.xml')
    xml_data = xml_factory.parsed_data
    liars = xml_data.findall(f".//person[lastName='Liar']")
    print(f'found: {len(liars)} persons')
    for liar in liars:
        firstname = liar.find('firstName').text
        print(f'first name: {firstname}')
        lastname = liar.find('lastName').text
        print(f'last name: {lastname}')
        [print(f"phone number ({p.attrib['type']}):", p.text) for p in liar.find('phoneNumbers')]
        print()


main()
