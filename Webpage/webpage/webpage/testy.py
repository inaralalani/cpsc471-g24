import duckdb
import numpy
db = duckdb.connect('m2kdashboard.db')
print(db.sql("SHOW ALL TABLES"))
print(db.sql("SELECT * FROM MarketingInstances").fetchnumpy().get('labeller_id'))
testy = db.sql("SELECT * FROM MarketingInstances").fetchnumpy().get('labeller_id')
testy.sort()