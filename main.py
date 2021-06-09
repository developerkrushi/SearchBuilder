import configmodel as cm
import os
import pandas as pd


# read Excel sheet
def readExcel(excel) -> tuple:
    inputData = pd.read_excel(excel, 'Input')
    outputData = pd.read_excel(excel, 'Output')
    joinData = pd.read_excel(excel, 'Joins')
    details = pd.read_excel(excel, 'Details')
    metadata = details.set_index('Field').T.to_dict('list')

    return inputData, outputData, joinData, metadata


# generate
def generateZipFile():
    cwd = os.getcwd()
    searchConfigPath = os.path.join(cwd, 'Output', 'searches')
    configPath = os.path.join(cwd, 'Output')
    dataModelConfigPath = os.path.join(cwd, 'Output', 'data-model-config')

    if os.path.exists(searchConfigPath):
        pass
    else:
        os.makedirs(searchConfigPath)

    if os.path.exists(dataModelConfigPath):
        pass
    else:
        os.makedirs(dataModelConfigPath)

    files = [cm.searchesConfig(searchConfigPath), cm.config(configPath), cm.dataModelConfig(dataModelConfigPath),
             cm.configProperties(configPath), cm.xformHTML(searchConfigPath)]

    cm.zipFiles(files, configPath)


inputData, outputData, joinData, metadata = readExcel('input.xlsx')

if __name__ == '__main__':
    generateZipFile()
