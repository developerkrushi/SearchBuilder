import pandas as pd

class DataSet:

    # TODO - perform data verification before conversion
    def dataVerification(self) -> bool:
        return True

    def inputTables(self, inputData: pd.DataFrame) -> dict:

        inputData = inputData[['Table', 'Input']].fillna('None')
        data = {}

        for index in inputData.index:

            if inputData['Table'][index] != 'None':
                table = ''
                cols = []
                table = inputData['Table'][index]
                cols.append(inputData['Input'][index])
            else:
                cols.append(inputData['Input'][index])

            data[table] = cols

        return data

    def joinsData(self,joinData: pd.DataFrame) -> dict:

        joinData[['Primary Table', 'Primary Key']] = joinData[['Primary Table', 'Primary Key']].fillna(method='ffill')
        joinDf = joinData[['Secondary Table', 'Foreign Key', 'Primary Table', 'Primary Key']]
        joinParameters = joinDf.set_index('Secondary Table').T.to_dict('list')

        return joinParameters

    def inputFlags(self, inputData: pd.DataFrame) -> dict:

        # Create a dictionary with input flag parameters ( Range, WildCard, Encryption )
        inputColumnDf = inputData[['Input', 'Date', 'Range', 'WildCard', 'Encryption', 'JulianDate']]
        inputFlags = inputColumnDf.set_index('Input').T.to_dict('list')

        return inputFlags

    def outputTables(self, outputData: pd.DataFrame) -> dict:

        outputData = outputData[['Table', 'Output']].fillna('None')
        data = {}

        for index in outputData.index:

            if outputData['Table'][index] != 'None':
                table = ''
                cols = []
                table = outputData['Table'][index]
                cols.append(outputData['Output'][index])
            else:
                cols.append(outputData['Output'][index])

            data[table] = cols

        return data

    def outputFlags(self, outputData: pd.DataFrame):
        # Create a dictionary with download flags for the output fields
        outputColumnDf = outputData[['Output', 'Download', 'Decrypt']]
        outputFlags = outputColumnDf.set_index('Output').T.to_dict('list')

        return outputFlags

    def getData(self) -> tuple:
        inputData = [{'table': 'TABLE1', 'columns': [{'name': 'col1', 'range': True, 'encryption': True},
                                                {'name': 'col2', 'range': False, 'encryption': False}], 'joins': []},
                {'table': 'TABLE2', 'columns': [{'name': 'col1', 'range': False, 'encryption': True},
                                                {'name': 'col2', 'range': True, 'encryption': False}],
                 'joins': [{'secondaryColumn': 'col1', 'primaryTable': 'TABLE1', 'primaryColumn': 'col2'}]}]

        outputData = [
            {'table': 'TABLE1', 'columns': [{'name': 'col1', 'download': False}, {'name': 'col2', 'download': True}]},
            {'table': 'TABLE2', 'columns': [{'name': 'col1', 'download': False}, {'name': 'col2', 'download': True}]}]

        return inputData, outputData
