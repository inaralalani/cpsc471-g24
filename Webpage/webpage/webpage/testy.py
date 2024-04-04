import duckdb
db = duckdb.connect("m2k.duckdb")
print(db.sql("SHOW ALL TABLES"))