import os


class Utility:

    @staticmethod
    def read_contents_from_file(filename):
        with open(filename, 'r', encoding="utf8") as reader:
            content = reader.read()
        return content

    @staticmethod
    def error(method, message):
        raise Exception('Error :- [{0}] {1}'.format(method, message))

    @staticmethod
    def check_integrity(filename):
        filepath_exists = os.path.isfile(filename)
        return filepath_exists

    @staticmethod
    def log(method, message):
        print('Log Message :- [{0}] {1}'.format(method, message))
