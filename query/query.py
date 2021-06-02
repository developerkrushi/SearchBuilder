import query.model as md
import pandas as pd


def readExcel(excel) -> tuple:
    inputData = pd.read_excel(excel, 'Input')
    outputData = pd.read_excel(excel, 'Output')
    joinData = pd.read_excel(excel, 'Joins')
    details = pd.read_excel(excel, 'Details')
    metadata = details.set_index('Field').T.to_dict('list')

    return inputData, outputData, joinData, metadata


def query():
    inputData, outputData, joinData, metadata = readExcel('input.xlsx')

    string = md.mainFunction(inputData, outputData, joinData, metadata)

    # with open('query.txt', 'w') as file:
    #     file.write(string)

    return string


if __name__ == '__main__':
    query()

