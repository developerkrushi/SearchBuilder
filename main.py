import configmodel as cm
import os


if __name__ == '__main__':
    
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
