import requests
import os
import sys
import csv
import inquirer
from datetime import datetime, date, timedelta
from invoke import run
sys.path.insert(0, "./app/utils")

from wikipedia_table import parse_table

CONFIRMED_I = 1
DEATHS_I = 4
RECOVERED_I = 5
[PROV_I, DAY_I, CONF_I, MUER_I, REC_I, CONF_T_I, MUER_T_I, REC_T_I] = [0, 1, 2, 3, 4, 5, 6, 7]

DATA_PADDING = 4

MESES = [
    "enero",
    "febrero",
    "marzo",
    "abril",
    "mayo",
    "junio",
    "julio",
    "agosto",
    "septiembre",
    "octubre",
    "noviembre",
    "diciembre"
]

PROVINCIAS = [
    "Provincia de Buenos Aires",
    "Catamarca",
    "Chaco",
    "Chubut",
    "Córdoba",
    "Corrientes",
    "Formosa",
    "Jujuy",
    "Mendoza",
    "Misiones",
    "Neuquén",
    "Salta",
    "Tucumán",
    "Entre Ríos",
    "La Pampa",
    "La Rioja",
    "Río Negro",
    "San Juan",
    "San Luis",
    "Santa Cruz",
    "Santa Fe",
    "Santiago del Estero",
    "Tierra del Fuego, Antártida e Islas del Atlántico Sur",
    "Ciudad Autónoma de Buenos Aires"
]


class AddEntry:
    def __init__(self):
        self.data_folder = "app/data"
        self.all_file = os.path.join(self.data_folder, "time_series_export.csv")
        self.process()

    def find_row(self, province, date, rows):
        for row in rows:
            if bool(row) and row['Provincia'] == province and row['Dia'] == date:
                return row

    def update_totals(self, province, rows):
        found_before = False
        [confirmed_total, deaths_total, recovered_total] = [0, 0, 0]

        for row in rows:
            if row[PROV_I] == province:
                # increment totals
                confirmed_total += int(row[CONF_I])
                deaths_total += int(row[MUER_I])
                recovered_total += int(row[REC_I])
                # set totals
                row[CONF_T_I] = confirmed_total
                row[MUER_T_I] = deaths_total
                row[REC_T_I] = recovered_total
                found_before = True
            elif found_before:
                # its sorted so avoid iterating over other provinces
                break

    def new_row(self, answers, day):
        return {
            "Provincia": answers['provincia'],
            "Dia": day,
            "Confirmados": answers['confirmados'],
            "Muertes": answers['muertes'],
            "Recuperados": answers['recuperados'],
            "Total Confirmados": 0,
            "Total Muertes": 0,
            "Total Recuperados": 0,
        }

    def updateCsv(self, answers):
        header = [
            "Provincia",
            "Dia",
            "Confirmados",
            "Muertes",
            "Recuperados",
            "Total Confirmados",
            "Total Muertes",
            "Total Recuperados",
        ]
        rows = list(csv.DictReader(open(self.all_file, "r")))
        day = f"{answers['mes']}/{answers['dia']}/{answers['año']}"

        row = self.find_row(answers['provincia'], day, rows)

        if row:
            row['Confirmados'] = int(answers['confirmados'])
            row['Muertes'] = int(answers['muertes'])
            row['Recuperados'] = int(answers['recuperados'])
        else:
            row = self.new_row(answers, day)
            rows.append(row)

        with open(self.all_file, "w") as f:
            writer = csv.writer(f)
            csv_rows = list(map(self.to_list, rows))
            csv_rows.sort(key=lambda _row: (_row[PROV_I], self.to_date(_row[DAY_I])))
            self.update_totals(answers['provincia'], csv_rows)
            writer.writerow(header)
            writer.writerows(csv_rows)

    def to_date(self, date_time_str):
        return datetime.strptime(date_time_str, '%m/%d/%y')

    def to_list(self, row):
        return [
            row['Provincia'],
            row['Dia'],
            row['Confirmados'],
            row['Muertes'],
            row['Recuperados'],
            row['Total Confirmados'],
            row['Total Muertes'],
            row['Total Recuperados'],
        ]

    def parseInput(self) -> dict:
        today = date.today()
        yesterday = today - timedelta(days=1)

        questions = [
          inquirer.List('provincia',
                        message="Elija su provincia",
                        choices=PROVINCIAS
                        ),
          inquirer.Confirm('ayer', message=f"Cargar datos de ayer? [{yesterday}]"),
          inquirer.Text('año', message="Año (2 digitos)",
                        default=today.strftime('%y'),
                        ignore=lambda ans: ans["ayer"],
                        validate=self.isNumber),
          inquirer.List('mes',
                        message="Mes",
                        choices=MESES,
                        ignore=lambda ans: ans["ayer"]),
          inquirer.Text('dia',
                        message="dia",
                        ignore=lambda ans: ans["ayer"],
                        validate=self.isNumber),
          inquirer.Text('confirmados', message='Confirmados',
                        validate=self.isNumber),
          inquirer.Text('muertes', message='Muertes',
                        validate=self.isNumber),
          inquirer.Text('recuperados', message='Recuperados',
                        validate=self.isNumber)
        ]
        answers = inquirer.prompt(questions)
        if answers["ayer"]:
            answers["dia"] = yesterday.strftime('%-d')
            answers["mes"] = yesterday.strftime('%-m')
            answers["año"] = yesterday.strftime('%y')
        else:
            answers["mes"] = self.parse_month(answers["mes"])
        return answers

    def process(self):
        answers = self.parseInput()
        summary = f"""
        provincia: {answers['provincia']}
        fecha: {answers['dia']}/{answers['mes']}/{answers['año']}
        confirmados: {answers['confirmados']}
        muertes: {answers['muertes']}
        recuperados: {answers['recuperados']}
        """
        print("Estas por ingresar:")
        print(summary)
        confirm = inquirer.prompt([inquirer.Confirm('yes', message='Desea continuar?')])
        if confirm["yes"]:
            print("Actualizando csv...")
            self.updateCsv(answers)
            print("Subiendo archivo...")
            self.commit(summary)
            print("Listo!")
        else:
            print("Abortando. Empezá de vuelta")

    def commit(self, summary):
        run("git checkout data-entry")
        run("git pull")
        run(f"git add {self.all_file}")
        run(f"git commit -m '{summary}'")
        run("git push")

    def parse_month(self, month):
        months = {
            "enero": 1,
            "febrero": 2,
            "marzo": 3,
            "abril": 4,
            "mayo": 5,
            "junio": 6,
            "julio": 7,
            "agosto": 8,
            "septiembre": 9,
            "octubre": 10,
            "noviembre": 11,
            "diciembre": 12
            }
        return months[month]

    def isNumber(self, answers, current):
        try:
            int(current)
            return True
        except Exception as e:
            return False

if __name__ == "__main__":
    AddEntry()
