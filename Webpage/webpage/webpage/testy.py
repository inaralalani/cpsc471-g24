import duckdb
import numpy
db = duckdb.connect('user key.duckdb')
print(db.sql("SELECT * FROM KEY WHERE Usertype!='researcher'"))