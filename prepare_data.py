import sqlite3
import pandas

industries = {
    '------': 'all',
    '51----': 'Information',
    '518///': 'Data Processing, Hosting, and Related Services',
    '11----': 'Agriculture, Forestry, Fishing and Hunting',
    '21----': 'Mining, Quarrying, and Oil and Gas Extraction',
    '52----': 'Finance and Insurance',
    '54----': 'Professional, Scientific, and Technical Services',
    '62----': 'Health Care and Social Assistance',
    '71----': 'Arts, Entertainment, and Recreation',
}


def disp(naics):
    return 'n' + naics.replace('-', '0').replace('/', '0')

con = sqlite3.connect('cbp.db')
con.cursor().execute('DROP TABLE IF EXISTS industries')
con.cursor().execute('CREATE TABLE industries (naics STRING, desc STRING)')

for naics in industries:
    con.cursor().execute('INSERT INTO industries VALUES (?, ?)', (disp(naics), industries[naics]))
con.commit()

for year in range(2007, 2015):
    file = 'data/Cbp%02dco.txt' % (year - 2000)
    df = pandas.read_csv(file)
    df['fips'] = df['fipstate'] * 1000 + df['fipscty']
    df = df.set_index('fips')
    for naics in industries:
        df2 = df.query('naics == "{}"'.format(naics))[['ap', 'emp', 'est']]
        df2.to_sql('{}_{}'.format(disp(naics), year), con, if_exists='replace')
        con.commit()
    print(year)

con.close()
