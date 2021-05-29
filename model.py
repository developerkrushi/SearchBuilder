import pandas as pd
from DataSet import DataSet
ds = DataSet()
class Model:

    # return the namespace definitions
    def declareNamespace(self) -> str:

        string = ('declare namespace ia = (: :) "urn:x-emc:ia:schema:fn";\n'
                  'declare namespace table = (: :)  "urn:x-emc:ia:schema:table";\n')
        return string

    def declareVariables(self, variables: list) -> str:
        string =('declare variable $page external;\n'
                 'declare variable $size external;\n')

        for x in variables:
            string += 'declare variable $' + str(x) + ' external := \'\';\n'

        string += '\ndeclare variable $limit := 2000;\n\n'

        return string

    def encryptFunction(self):
        string = ('declare function ia:create-encrypted-condition($expressionStr as xs:string, $operator as xs:string, $columnValue as xs:string*) as xs:string external;\n'
                  'declare function ia:decrypt-value($columnValue as xs:string*) as xs:string* external;\n')

        return string

    # return the definition of addClause function
    def addClause(self) -> str:

        string = ('declare function local:addClause($var xs:string*, $expr as xs:string*) as xs:string* {\n'
                  '    if (empty($var) or $var = "" or normalize-space($var) = "") then ""\n'
                  '    else concat("[", $expr , "]") \n'
                  '};\n')

        return string

    def addClauseWild(self) -> str:
        string = ('declare function local:addClauseWild($var as xs:string*, $col as xs:string) as xs:string {\n'
                  '    if (empty($var) or $var = '' or normalize-space($var) = '') then ""\n'
                  '    else\n'
                  '    let $x := if (matches($var,".*")) then $var else concat(\'.*\',$var,\'.*\')\n'
                  '    let $y := concat($col,\' contains text {".*\',$x,\'.*"} using wildcards \')\n'
                  '  return concat("[", $y , "]")\n'
                  '};\')')

        return string
    # return the definition of getResultsPage function
    def getResultsPage(self) -> str:

        string = ('declare function local:getResultsPage($rows, $page, $size) {\n'
                  '    let $offset := $page * $size let $total := count($rows)\n'
                  '    return   <results total="{ $total }">    {\n'
                  '               for $row in subsequence($rows, $offset + 1, $size)\n'
                  '                 return $row\n'
                  '               }\n'
                  '             </results>\n'
                  '};\n')

        return string

    # return function definition for WildCard
    def addClauseWild(self) -> str:
        string = ("declare function local:addClauseWild($var as xs:string*, $col as xs:string) as xs:string {\n"
                  "    if (empty($var) or $var = '' or normalize-space($var) = '') then ''\n"
                  "    else\n"
                  "      return '[contains($col,'\",$var,\"')]'\n"
                  "};\n")

        return string

    def julianDate(self) -> str:
        string = ('declare function local:julianDateConversion($value as xs:string*) as xs:string*{\n'
                  '    let $returnValue := ""\n'
                  '    let $strVal := string-length($value)\n'
                  '    let $assertSixDigitsString := if(xs:integer($strVal) = 5) then concat("0",$value) else $value\n'
                  '    let $century := (19 + xs:integer(substring($assertSixDigitsString, 1, 1))) * 100\n'
                  '    let $year := xs:integer($century) + xs:integer(substring($assertSixDigitsString,2,2))\n'
                  '    let $numberOfDays := xs:integer(substring($assertSixDigitsString,4)) - 1\n'
                  '    let $startDate := concat($year, "-01-01")\n'
                  '    let $timeDuration := concat("P",$numberOfDays,"D")\n'
                  '    let $returnValue := xs:string(xs:date(normalize-space(data($startDate))) + xs:dayTimeDuration($timeDuration))\n\n'
                  '    return $returnValue\n'
                  '};\n')

        return string

    # declare and define a variable
    def createVariable(self, name: str, value: str) -> str:
        string = "let $" + name + " := " + value

        return string

    # returns Main Query part
    def queryString(self, schema: str, tableData: dict, inputFlags: dict, joinData: dict) -> str:
        string = 'concat(\n'
        string += '\t\t\t\t'

        # generates for loop statements
        for table in tableData:
            string += '" for $' + table + ' in ' + schema + '/' + table + '/ROW'

            # attach join conditions
            stringJoin = ''
            if table in joinData:
                keys = joinData[table]
                stringJoin = '[' + keys[0] + '=' + '$' + keys[1] + '/' + keys[2] + ']'
            string += stringJoin +'",\n'
            string += '\t\t\t\t'


            for column in tableData[table]:
                flags = inputFlags[column]
                if flags[0] == 'y' and flags[1] == 'y' and flags[3] == 'y':
                    string += 'local:addClause($' + column + '/from, ia:create-encrypted-condition(\'' + column + '\', \'>=\', $' + column + '/from)),\n'
                    string += '\t\t\t\t'
                    string += 'local:addClause($' + column + '/to, ia:create-encrypted-condition(\'' + column + '\', \'<=\', $' + column + '/to)),\n'
                    string += '\t\t\t\t'
                elif flags[1] == 'y' and flags[3] == 'y':
                    string += 'local:addClause($' + column + ', ia:create-encrypted-condition(\'' + column + '\', \'>=\', $' + column + ')),\n'
                    string += '\t\t\t\t'
                    string += 'local:addClause($' + column + ', ia:create-encrypted-condition(\'' + column + '\', \'<=\', $' + column + ')),\n'
                    string += '\t\t\t\t'
                elif flags[0] == 'y' and flags[1] == 'y':
                    string += 'local:addClause($' + column + '/from, concat("substring(' + column + ',1,10) >= \'", substring($' + column + '/from,1,10), "\'")),\n'
                    string += '\t\t\t\t'
                    string += 'local:addClause($' + column + '/to, concat("substring(' + column + ',1,10) <= \'", substring($' + column + '/to,1,10), "\'")),\n'
                    string += '\t\t\t\t'
                elif flags[1] == 'y':
                    string += 'local:addClause($' + column + ', concat("' + column + ' >= \'", $' + column + ', "\'")),\n'
                    string += '\t\t\t\t'
                    string += 'local:addClause($' + column + ', concat("' + column + ' <= \'", $' + column + ', "\'")),\n'
                    string += '\t\t\t\t'
                elif flags[3] == 'y':
                    string += 'local:addClause($' + column+ ', ia:create-encrypted-condition(\'' + column + '\', \'=\', $' + column + ')),\n'
                    string += '\t\t\t\t'
                elif flags[2] == 'y':
                    string += 'local:addClauseWild($' + column + ', \'' + column + '\'),\n'
                    string += '\t\t\t\t'
                elif flags[0] == 'y':
                    string += 'local:addClause($' + column + ', concat("substring(' + column + ',1,10) = \'", substring($' + column + ',1,10), "\'")),\n'
                    string += '\t\t\t\t'
                else:
                    string += 'local:addClause($' + column + ', concat("' + column + ' = \'", $' + column + ', "\'")),\n'
                    string += '\t\t\t\t'


        string += '" return ")'

        return string

    def returnString(self, data: dict, outputFlags: dict) -> str:
        primaryTable = list(data.keys())[0]

        string = '<row id=\'{string($' + primaryTable + '/@table:id)}\'>\n'
        string += '\t\t\t\t'

        for table in data:
            for column in data[table]:
                download = list(outputFlags[column])[0]
                decrypt = list(outputFlags[column])[1]
                if download == 'y':
                    string += '<column name=\'' + column + '\'>{$' + table + '/' + column + '/@ref/string()}</column>\n'
                    string += '\t\t\t\t'
                elif decrypt == 'y':
                    string += '<column name=\'' + column + '\'>{ia:decrypt-value($' + table + '/' + column + '/string())}</column>\n'
                    string += '\t\t\t\t'
                else:
                    string += '<column name=\'' + column + '\'>{$' + table + '/' + column + '/string()}</column>\n'
                    string += '\t\t\t\t'
        string += '</row>'

        return string

    def mainFunction(self, inputData: pd.DataFrame, outputData: pd.DataFrame, joinData: pd.DataFrame) -> str:

        schema = inputData['Schema'].tolist()[0]

        tableData = ds.inputTables(inputData)
        inputFlags = ds.inputFlags(inputData)
        joinData = ds.joinsData(joinData)
        inputColumns = inputData['Input'].tolist()

        wildCardFields = inputData['WildCard'].tolist()
        wildCard = False
        if 'y' in wildCardFields:
            wildCard = True

        encryptionFeilds = inputData['Encryption'].tolist()
        encryption = False
        if 'y' in encryptionFeilds:
            encryption = True

        julianFields = inputData['JulianDate'].tolist()
        julianDate = False
        if 'y' in julianFields:
            julianDate = True

        outputTables = ds.outputTables(outputData)
        downloadFlags = ds.outputFlags(outputData)

        string = ''

        declarationSection = '(: :::::::::::::::::: Declaration and Initialization  of Variables, Namespaces :::::::::::::::::::: :)\n\n'
        declarationSection += self.declareNamespace() + self.declareVariables(inputColumns)

        if encryption:
            declarationSection += self.encryptFunction() + '\n'

        defaultFunctions = '(: :::::::::::::::::::::::::::::::: Function definitions :::::::::::::::::::::::::::::::::::: :)\n\n'
        defaultFunctions += self.addClause() + '\n'

        if wildCard:
            defaultFunctions += self.addClauseWild() + '\n'

        if julianDate:
            defaultFunctions += self.julianDate() + '\n'

        defaultFunctions += self.getResultsPage()

        mainSection = '(: :::::::::::::::::::::::::::::::: Main Function definition :::::::::::::::::::::::::::::::::::: :)\n\n'
        mainSection += 'declare function local:MAIN('
        for column in inputColumns:
            mainSection += '$' + column + ', '

        mainSection += '$limit, $page, $size) {\n\n'

        mainSection += ('    let $import := \'declare namespace ia = (: :) "urn:x-emc:ia:schema:fn";\n'
                        '                    declare namespace table = (: :)  "urn:x-emc:ia:schema:table";\'')

        mainSection += '\n\n\t' + self.createVariable('query', self.queryString(schema, tableData, inputFlags, joinData))

        mainSection += '\n\n\t' + self.createVariable('return', '"' + self.returnString(outputTables, downloadFlags) + '"')

        mainSection += '\n\n\t' + self.createVariable('mainQuery', 'subsequence(xhive:evaluate(concat($import,$query,$return)),1,$limit)')

        mainSection += ('\n\n\treturn local:getResultsPage($mainQuery, $page, $size)\n'
                        '};\n\n'
                        '(: :::::::::::::::::::::::::::::::: Main Function Call :::::::::::::::::::::::::::::::::::: :)\n'
                        'local:MAIN(')

        for column in inputColumns:
            mainSection += '$' + column + ', '

        mainSection += '$limit, $page, $size)'


        string += declarationSection + defaultFunctions + '\n\n' + mainSection

        return string
