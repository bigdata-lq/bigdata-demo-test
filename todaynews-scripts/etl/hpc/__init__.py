coreTableResult = ['aaa', 'aaa1', 'aaa2']

tableCoreDict = {'aaa':'1' ,'aaa1':'2', 'aaa2':'1'}

tableName = 3
for name in coreTableResult :
    if tableName in tableCoreDict.keys():
        tableCoreDict[name] = tableCoreDict[name] + '.'+ tableName
    else:
        tableCoreDict[name] = tableName

print(tableCoreDict)