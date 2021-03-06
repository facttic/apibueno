# Variables needed in order: url of the database host, username of database, datab name

host=$1
user=$2
db=$3

cd app/data
# removes the first line (column names)
sed -i 1d time_series_export.csv


# Connects to remote databse (password promt)
# truncates database to insert new data
# Sets data format to read correctly from csv
# runs inserts from local CSV file
psql -h $host -p 5432 -U $user $db  << EOF
TRUNCATE TABLE covid_timeseries;
SET datestyle = mdy;
\copy "covid_timeseries" FROM 'time_series_export.csv' CSV;
EOF
###


