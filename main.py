from model import Model
from DataSet import DataSet
import pandas as pd
import datetime

md = Model()
ds = DataSet()


def codeBrief(metadata: dict) -> str:
    searchName = metadata['Search'][0]
    appName = metadata['Application'][0]
    author = metadata['Author'][0]
    date = datetime.date.today()

    string = ('(:~\n'
              '::\n'
              f':: Application Name: {appName}\n'
              '::\n'
              f':: Search Name: {searchName}\n'
              '::\n'
              '::\n'
              ':: Copyright: Medtronic\n'
              '::\n'
              f':: @author {author}\n'
              f':: @since {date.strftime("%b %d, %Y")}\n'
              ':: @version 1.0\n'
              ':)\n\n')

    return string


def readExcel(excel) -> tuple:
    inputData = pd.read_excel(excel, 'Input')
    outputData = pd.read_excel(excel, 'Output')
    joinData = pd.read_excel(excel, 'Joins')
    details = pd.read_excel(excel, 'Details')
    metadata = details.set_index('Field').T.to_dict('list')

    return inputData, outputData, joinData, metadata


def main():
    inputData, outputData, joinData, metadata = readExcel('input.xlsx')

    string = md.mainFunction(inputData, outputData, joinData)
    codeHeader = codeBrief(metadata)

    with open('query.txt', 'w') as file:
        file.write(codeHeader)
        file.write(string)


if __name__ == '__main__':
    main()

