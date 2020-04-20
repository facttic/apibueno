import os
import sys
import csv
from datetime import datetime

class ExportCSV:
    def __init__(self):
        self.data_folder = "app/data"
        self.confirmed_file = os.path.join(self.data_folder, "time_series_confirmed.csv")
        self.deaths_file = os.path.join(self.data_folder, "time_series_deaths.csv")
        self.recovered_file = os.path.join(self.data_folder, "time_series_recovered.csv")
        self.export_file = os.path.join(self.data_folder, "time_series_export.csv")
        self.process()

    def process(self):
        # load csvs into memory
        confirmed_read = self.load_csv(self.confirmed_file)
        deaths_read = self.load_csv(self.deaths_file)
        recovered_read = self.load_csv(self.recovered_file)

        with open(self.export_file, "w") as c:
            export = csv.writer(c)
            items = []
            header = [
                'Provincia',
                'Dia',
                'Confirmados',
                'Muertes',
                'Recuperados',
                'Total Confirmados',
                'Total Muertes',
                'Total Recuperados'
            ]
            for i, row in enumerate(confirmed_read):
                if i == 0:
                    days = row[4:]
                    export.writerow(header)
                else:
                    province = row[0]
                    confirmed_total = 0
                    deaths_total = 0
                    recovered_total = 0
                    for j, day in enumerate(row[4:]):
                        confirmed_row = day
                        deaths_row = deaths_read[i][j+4]
                        recovered_row = recovered_read[i][j+4]
                        # totals
                        confirmed_total += int(confirmed_row)
                        deaths_total += int(deaths_row)
                        recovered_total += int(recovered_row)
                        item = [
                            province,
                            days[j],
                            confirmed_row,
                            deaths_row,
                            recovered_row,
                            confirmed_total,
                            deaths_total,
                            recovered_total
                        ]
                        items.append(item)
            export.writerows(items)

    def load_csv(self, file_path):
        rows = []
        file = open(file_path, "r")
        from_csv = csv.reader(file)
        rows.extend(from_csv)
        return rows

if __name__ == "__main__":
    ExportCSV()
