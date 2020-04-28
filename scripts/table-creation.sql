DROP TABLE IF EXISTS "covid_timeseries";
CREATE TABLE IF NOT EXISTS "covid_timeseries" (
    "Provincia" TEXT,
    "Dia" DATE,
    "Confirmados" INT,
    "Muertes" INT,
    "Recuperados" INT,
    "Total Confirmados" INT,
    "Total Muertes" INT,
    "Total Recuperados" INT
);
