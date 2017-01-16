import sqlite3


class Model:
    def __init__(self, con):
        self.con = con
        print("Model started")

    def get_years(self):
        return range(2007, 2015)

    def get_industries(self):
        cur = self.con.cursor()
        cur.execute('SELECT * FROM industries')
        result = dict()
        for k, v in cur.fetchall():
            result[k] = v
        return result

    def get_data(self, naics, year, expr):
        cur = self.con.cursor()
        cur.execute('SELECT fips, {} AS value FROM {}_{}'.format(expr, naics, year))
        result = dict()
        for fips, value in cur.fetchall():
            result[fips] = value
        return result


if __name__ == '__main__':
    model = Model(sqlite3.connect('cbp.db'))
    print(model.get_years())
    print(model.get_industries())
    print(model.get_data('n000000', 2010, 'emp'))



