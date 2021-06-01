import query.query as qy

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


print(qy.main())