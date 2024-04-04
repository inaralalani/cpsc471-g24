import duckdb as ddb

con = ddb.connect("m2kdashboard.db")

con.read_csv("data/*.csv")
con.sql("CREATE OR REPLACE TABLE Labels AS SELECT * FROM 'data/LABELS.csv';")
con.sql("CREATE OR REPLACE TABLE Foods AS SELECT * FROM 'data/FOODS.csv';")
con.sql("CREATE OR REPLACE TABLE Marketing AS SELECT * FROM 'data/MARKETING.csv';")
con.sql("CREATE OR REPLACE TABLE Techniques AS SELECT * FROM 'data/TECHNIQUES.csv';")
con.sql("CREATE OR REPLACE TABLE Users AS SELECT * FROM 'data/USERS.csv';")

