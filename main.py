import configmodel as cm
import os

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


def createConfigFiles():
    files = [cm.searchesConfig(searchConfigPath), cm.config(configPath), cm.dataModelConfig(dataModelConfigPath),
             cm.configProperties(configPath), cm.xformHTML(searchConfigPath)]

    cm.zipFiles(files, configPath)


if __name__ == '__main__':
    createConfigFiles()
