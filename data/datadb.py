import duckdb as ddb
con = ddb.connect("m2kdashboard.db")

ddb.read_csv("LABELS.csv")
ddb.read_csv("FOODS.csv")
ddb.read_csv("MARKETING.csv")
ddb.read_csv("TECHNIQUES.csv")
ddb.read_csv("USERS.csv")



