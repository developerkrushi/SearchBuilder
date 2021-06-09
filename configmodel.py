import query.model as md
import pandas as pd
import yaml
import os
import datetime
from zipfile import ZipFile
import shutil
from main import *

#inputData, outputData, joinData, metadata = qy.readExcel('input.xlsx')


def version() -> dict:
    return {'version': '1.0.0'}


def application(appname: str) -> dict:
    return {'application': {'name': appname, 'configure': 'use existing'}}


def tenant() -> dict:
    return {'tenant': {'name': 'INFOARCHIVE', 'configure': 'use existing'}}


def includes() -> dict:
    return {'includes': ['data-model-config/configuration.yml', 'searches/configuration.yml']}


def database(appname: str) -> dict:
    return {'database': {'name': appname + '-sql-db', 'configure': 'use existing'}}


def resultMaster(outputdata: pd.DataFrame, metadata: dict):
    columns = outputdata['Output'].tolist()
    labels = outputdata['Label'].tolist()
    columnsList = []
    downloadFlags = outputdata['Download'].tolist()
    appName = metadata['Application'][0]

    for column in columns:
        i = columns.index(column)
        if downloadFlags[i] == 'y':
            dictColumn = {'name': column,
                          'cellLabel': 'Click Here',
                          'contentLinkType': 'CUSTOM',
                          'dataType': 'CID',
                          'label': 'Download',
                          'type': 'content'}

        else:
            dictColumn = {'name': column,
                          'contentLinkType': 'CUSTOM',
                          'label': labels[i],
                          'type': 'xquery reference'}

        columnsList.append(dictColumn)

        tabList = [{'name': '_ia_Default_Main_tab_', 'columns': columnsList}]
        panelsList = [{'name': 'Inline Panel'}, {'name': 'Main Panel', 'tabs': tabList}, {'name': 'Side Panel'}]

        resultMasterDict = {'application': appName, 'panels': panelsList, 'tenant': 'INFOARCHIVE'}
        resultMasterToken = {'resultMaster': resultMasterDict}

    return resultMasterToken


def search(inputdata: pd.DataFrame, metadata: dict):
    schema = inputdata['Schema'].tolist()[0]
    searchName = metadata['Search'][0]
    searchDesc = metadata['SearchDescription'][0]

    return {'search':
                {'name': searchName,
                 'aic': None,
                 'description': searchDesc,
                 'query': None,
                 'schema': schema,
                 'state': '${search.state:published}'}}


def searchComposition():
    return {'searchComposition': {'name': 'Set 1'}}


def xform(metadata: dict):
    searchName = metadata['Search'][0]
    return {'xform': {'name': searchName, 'form': {'resource': f'xform-{searchName.replace(" ", "")}.html'}}}


def xquery(metadata: dict):
    searchName = metadata['Search'][0]
    return {'xquery': {'name': searchName, 'application': None, 'query': '\|'}}


def searchesConfig(path):
    path = os.path.join(path, 'configuration.yml')
    searchName = metadata['Search'][0]
    appName = metadata['Application'][0]
    query = md.mainFunction(inputData, outputData, joinData, metadata)

    dd = resultMaster(outputData, metadata)
    dl = xquery(metadata)

    with open(path, 'w+') as file:
        ver = version()
        yaml.dump(ver, file, default_style=None, default_flow_style=False, sort_keys=False)
        file.write('\n')

        ten = tenant()
        yaml.dump(ten, file, default_style=None, default_flow_style=False, sort_keys=False)
        file.write('\n')

        app = application(appName)
        yaml.dump(app, file, default_style=None, default_flow_style=False, sort_keys=False)
        file.write('\n')

        db = database(appName)
        yaml.dump(db, file, default_style=None, default_flow_style=False, sort_keys=False)
        file.write('\n')

        rm = resultMaster(outputData, metadata)
        yaml.dump(rm, file, default_style=None, default_flow_style=False, sort_keys=False)
        file.write('\n')

        sh = search(inputData, metadata)
        yaml.dump(sh, file, default_style=None, default_flow_style=False, sort_keys=False)
        file.write('\n')

        sc = searchComposition()
        yaml.dump(sc, file, default_style=None, default_flow_style=False, sort_keys=False)
        file.write('\n')

        xf = xform(metadata)
        yaml.dump(xf, file, default_style=None, default_flow_style=False, sort_keys=False)
        file.write('\n')

    with open(path, 'a') as file:
        file.write(('xquery:\n'
                    f'  name: {searchName}\n'
                    '  application: null\n'
                    '  query: |\n'))

        stringList = query.splitlines()
        for line in stringList:
            file.write('    ')
            file.write(line)
            file.write('\n')

    return path


def config(path):
    path = os.path.join(path, 'configuration.yml')
    appName = metadata['Application'][0]

    with open(path, 'w+') as file:
        ver = version()
        yaml.dump(ver, file, default_style=None, default_flow_style=False, sort_keys=False)
        file.write('\n')

        app = application(appName)
        yaml.dump(app, file, default_style=None, default_flow_style=False, sort_keys=False)
        file.write('\n')

        ten = tenant()
        yaml.dump(ten, file, default_style=None, default_flow_style=False, sort_keys=False)
        file.write('\n')

        inc = includes()
        yaml.dump(inc, file, default_style=None, default_flow_style=False, sort_keys=False)
        file.write('\n')

    return path


def dataModelConfig(path):
    path = os.path.join(path, 'configuration.yml')
    appName = metadata['Application'][0]

    with open(path, 'w+') as file:
        ver = version()
        yaml.dump(ver, file, default_style=None, default_flow_style=False, sort_keys=False)
        file.write('\n')

        ten = tenant()
        yaml.dump(ten, file, default_style=None, default_flow_style=False, sort_keys=False)
        file.write('\n')

        app = application(appName)
        yaml.dump(app, file, default_style=None, default_flow_style=False, sort_keys=False)
        file.write('\n')

        db = database(appName)
        yaml.dump(db, file, default_style=None, default_flow_style=False, sort_keys=False)
        file.write('\n')

    return path


def configProperties(path):
    path = os.path.join(path, 'configuration.properties')
    date = datetime.datetime.today()
    with open(path, 'w') as file:
        file.write(f'#{date.strftime("%a %b %d %H:%M:%S IST %Y")}\n')
        file.write('search.state=published\n')

    return path


def xformHTML(path):
    searchName = metadata['Search'][0]
    columns = inputData['Input'].tolist()
    labels = inputData['Label'].tolist()
    range = inputData['Range'].tolist()
    date = inputData['Date'].tolist()
    wild = inputData['WildCard'].tolist()
    path = os.path.join(path, f'xform-{searchName.replace(" ", "")}.html')

    with open(path, 'w') as file:
        file.write(('<xhtml:html xmlns:xhtml="http://www.w3.org/1999/xhtml" xmlns:xforms="http://www.w3.org/2002/xforms" xmlns:xsd="http://www.w3.org/2001/XMLSchema">\n'
                    '<xhtml:head>\n'
                    '    <xforms:model>\n'
                    '        <xforms:instance xmlns="">\n\n'
                    '        <data>\n'))

        file.write('            ')
        for column in columns:
            i = columns.index(column)
            if range[i] == 'y':
                file.write(f'<{column}><from/><to/></{column}>')

            else:
                file.write(f'<{column}/>')

        file.write(('</data></xforms:instance>'
                    '\n'        
                    '        <xforms:instance xmlns="" id="labels">\n\n'
                    '        <labels>'))

        for column in columns:
            i = columns.index(column)
            file.write(f'<{column}>{labels[i]}:</{column}>')

        file.write(('</labels></xforms:instance>'
                    '\n'        
                    '        <xforms:instance xmlns="" id="hints">\n\n'
                    '        <hints>'))

        for column in columns:
            file.write(f'<{column}/>')

        file.write(('</hints></xforms:instance>'
                    '\n'        
                    '        <xforms:instance xmlns="" id="prompts">\n\n'
                    '        <prompts>'))

        for column in columns:
            i = columns.index(column)
            if wild[i] == 'y' and range[i] != 'y':
                file.write(f'<{column}>Wildcard search available</{column}>')

            elif range[i] != 'y':
                file.write(f'<{column}/>')

        file.write(('</prompts></xforms:instance>'
                    '\n'        
                    '        <xforms:instance xmlns="" id="alerts">\n\n'
                    '        <alerts>'))

        for column in columns:
            file.write(f'<{column}/>')

        file.write(('</alerts></xforms:instance>'
                    '\n'        
                    '        <xforms:instance xmlns="" id="range-messages">\n\n'
                    '        <rangemessages>'))

        for column in columns:
            i = columns.index(column)
            if range[i] != 'y':
                file.write(f'<{column}/>')

        file.write(('</rangemessages></xforms:instance>'
                    '\n'        
                    '        <xforms:instance xmlns="" id="pattern-messages">\n\n'
                    '        <patternmessages>'))

        for column in columns:
            i = columns.index(column)
            if range[i] != 'y':
                file.write(f'<{column}/>')

        file.write(('</patternmessages></xforms:instance>'
                    '\n'        
                    '        <xforms:submission id="submit01" method="post" serialization="application/xml"/>\n'))

        file.write(('        <xsd:schema xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xforms="http://www.w3.org/2002/xforms" targetNamespace="http://www.w3.org/2002/xforms" elementFormDefault="qualified">\n'
                    '        </xsd:schema>\n'))
        file.write('    ')

        for column in columns:
            i = columns.index(column)
            if range[i] == 'y' and date[i] == 'y':
                file.write(f'<xforms:bind ref="/data/{column}/from" type="xforms:date" constraint="(string-length(.) = 0 or days-from-date(.) &lt;= days-from-date(/data/{column}/to))"/>'
                           f'<xforms:bind ref="/data/{column}/to" type="xforms:date" constraint="(string-length(.) = 0 or days-from-date(.) &gt;= days-from-date(/data/{column}/from))"/>')
            elif range[i] == 'y':
                file.write((f'<xforms:bind ref="/data/{column}/from" type="xforms:decimal" constraint="(string-length(.) = 0 or string-length(/data/{column}/to) = 0 or . &lt;= /data/{column}/to)"/>'
                            f'<xforms:bind ref="/data/{column}/to" type="xforms:decimal" constraint="(string-length(.) = 0 or string-length(/data/{column}/from) = 0 or . &gt;= /data/{column}/from)"/>'))
            else:
                file.write(f'<xforms:bind ref="/data/{column}"/>')

        file.write('</xforms:model>\n</xhtml:head>\n<xhtml:body>\n')

        for column in columns:
            i = columns.index(column)
            if range[i] == 'y':
                file.write(f'<input xmlns="http://www.w3.org/2002/xforms" ref="/data/{column}/from">'
                           f'<label ref="instance(\'labels\')/{column}"/>'
                           f'<hint ref="instance(\'hints\')/{column}"/>'
                           f'<hint appearance="minimal" ref="instance(\'prompts\')/{column}"/>'
                           f'<alert ref="instance(\'alerts\')/{column}"/>'
                           f'<message class="range" ref="instance(\'range-messages\')/{column}"/>'
                           f'<message class="pattern" ref="instance(\'pattern-messages\')/{column}"/></input>'
                           f'<input xmlns="http://www.w3.org/2002/xforms" ref="/data/{column}/to"/>')
            else:
                file.write(f'<input xmlns="http://www.w3.org/2002/xforms" ref="/data/{column}">'
                           f'<label ref="instance(\'labels\')/{column}"/>'
                           f'<hint ref="instance(\'hints\')/{column}"/>'
                           f'<hint appearance="minimal" ref="instance(\'prompts\')/{column}"/>'
                           f'<alert ref="instance(\'alerts\')/{column}"/>'
                           f'<message class="range" ref="instance(\'range-messages\')/{column}"/>'
                           f'<message class="pattern" ref="instance(\'pattern-messages\')/{column}"/></input>')

        file.write('</xhtml:body>\n</xhtml:html>')

    return path


def zipFiles(files, path):
    searchName = metadata['Search'][0]

    with ZipFile(f'{searchName}.zip', 'w') as zip:
        # writing each file one by one
        for file in files:
            #file = file.replace(path, 'Output')
            zip.write(file, file.replace(path, ''))

    shutil.rmtree(path)