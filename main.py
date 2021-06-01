import yaml

dic = {'version': '1.0.0',
       'application': {'name': 'Stellent', 'configure': 'use existing'},
       'tenant': {'name': 'INFOARCHIVE', 'configure': 'use existing'},
       'includes': ['data-model-config/configuration.yml', 'searches/configuration.yml']
        }

with open('configuration.yml', 'w') as file:
    yaml.dump(dic, file, default_flow_style=False, sort_keys=False)