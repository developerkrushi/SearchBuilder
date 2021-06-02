import pandas as pd


# TODO - perform data verification before conversion
def dataVerification() -> bool:
    return True


# Create data frame for input tables and columns
def inputTables(inputData: pd.DataFrame) -> dict:

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


# create data frame for join conditions
def joinsData(joinData: pd.DataFrame) -> dict:

    joinData[['Primary Table', 'Primary Key']] = joinData[['Primary Table', 'Primary Key']].fillna(method='ffill')
    joinDf = joinData[['Secondary Table', 'Foreign Key', 'Primary Table', 'Primary Key', 'Join']]
    joinParameters = joinDf.set_index('Secondary Table').T.to_dict('list')

    return joinParameters


# create data frame for input conditions
def inputFlags(inputData: pd.DataFrame) -> dict:

    # Create a dictionary with input flag parameters ( Range, WildCard, Encryption )
    inputColumnDf = inputData[['Input', 'Date', 'Range', 'WildCard', 'Encryption', 'JulianDate']]
    inputFlags = inputColumnDf.set_index('Input').T.to_dict('list')

    return inputFlags


# create data frame for output tables and columns
def outputTables(outputData: pd.DataFrame) -> dict:

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


# create data frame for output conditions
def outputFlags(outputData: pd.DataFrame):
    # Create a dictionary with download flags for the output fields
    outputColumnDf = outputData[['Output', 'Download', 'Decrypt']]
    outputFlags = outputColumnDf.set_index('Output').T.to_dict('list')

    return outputFlags
