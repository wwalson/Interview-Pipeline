import pyodbc

conn = pyodbc.connect(
    "DRIVER={ODBC Driver 18 for SQL Server};"
    "SERVER=localhost;"
    "DATABASE=UtilityAnalytics;"
    "Trusted_Connection=yes;"
    #had to add TrustServerCertificate=yes due to hosting on my local machine
    "TrustServerCertificate=yes;"
)

print("CONNECTED!")