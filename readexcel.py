import pandas
fd=pandas.read_excel('F:\\pytserver\\cscompany.xls',encoding='utf-8')
rows=fd[['Name','lon','lat']].values
with open('F:\\pytserver\\cscompany.txt','a') as f:
    index=0
    for row in rows:
        data=str(row[0])+","+str(row[1])+","+str(row[2])+";"
        index=index+1
        f.write(data)
    print(index)

    