# Argentina Covid19 API

> Este proyecto fue hecho en el marco de [Hacktic](https://hackdash.org/projects/5e8b6b87875b954b4a1d13fa), una Hackaton dónde participan múltiples cooperativas de [Facttic](https://facttic.org.ar/) y esta basado en [Coronavirus Tracker API](https://github.com/ExpDev07/coronavirus-tracker-api)

[![Contributor Covenant](https://img.shields.io/badge/Contributor%20Covenant-v2.0%20adopted-ff69b4.svg)](code_of_conduct.md)
[![License](https://img.shields.io/github/license/facttic/apibueno)](LICENSE.md)


## Objetivos

 - Disponibilizar datos del COVID-19 de cada provincia de Argentina, para que sea consumible por aplicaciones y cualquier persona que quiera usar los datos los pueda consultar, sabiendo que provienen solo de comunicaciones oficiales y que se actualizan todos los días. Hoy en dia existen varias de estas APIs a nivel internacional pero no contienen informacion a nivel local (solo discriminan a Argentina a nivel pais).
 - Tiene que estar documentada con Swagger para que sea consultable y "descubrible"

## Datos iniciales y carga manual

Los datos hasta el 15 de Abril fueron recopilados manualmente.
El procedimiento y fuentes de informacion estan detallados en **[este](/fuentes-de-datos-y-procedimiento.md)** documento.

<!--
## Actualizacion automatica

Evaluamos varias fuentes de datos:
- https://www.argentina.gob.ar/coronavirus/informe-diario
- https://github.com/SistemasMapache/Covid19arData
- https://es.wikipedia.org/wiki/Pandemia_de_enfermedad_por_coronavirus_de_2020_en_Argentina

En principio usamos la web de [Wikipedia Coronavirus Argentina](https://es.wikipedia.org/wiki/Pandemia_de_enfermedad_por_coronavirus_de_2020_en_Argentina) mientras encontramos la mejor manera de parsear los pdf a partir de los que informa el Ministerio de Salud.
-->
## API

Esta hecha en python con [FastApi](https://fastapi.tiangolo.com/)

Todos los endpoints estan documentados y son accesible vía https:

- [Swagger UI ApiBueno](https://apibueno.herokuapp.com/)
- [Redoc ApiBueno](https://apibueno.herokuapp.com/docs)

Podes usar el browser o por ejemplo hacer uso de curl en tu terminal:
`curl https://apibueno.herokuapp.com/v2/locations`

### OpenAPI

La definción json de [OpenAPI](https://swagger.io/docs/specification/about/) la podes bajar de [https://apibueno.herokuapp.com/openapi.json](https://apibueno.herokuapp.com/openapi.json)


## Instalación

* `git clone https://github.com/facttic/apibueno.git`
* `cd apibueno`

1. Tenes que tener [`python3.8` instalado en el `PATH`](https://docs.python-guide.org/starting/installation/).
2. [Instala `pipenv` como manejador de dependencias](https://pipenv.readthedocs.io/en/latest/install/#installing-pipenv)
3. Crea un ambiente virtual y instalar todas las dependencies `$ pipenv sync --dev`
4. Entrar al ambiente virtual `$ pipenv shell`

## Levantar entorno de Desarrollo

* `pipenv run dev`
* Ir a la aplicación en [http://localhost:8000](http://localhost:8000).

### Correr Tests
> [pytest](https://docs.pytest.org/en/latest/)

```bash
pipenv run test
```


### Linting
> [pylint](https://www.pylint.org/)

```bash
pipenv run lint
```

### Formateo
> [black](https://black.readthedocs.io/en/stable/)

```bash
pipenv run fmt
```

### Schedule
> Schedule scraping cada 24 horas

```bash
pipenv run schedule
```

### Scraping
> Scrapea wikipedia y agregar al CSV

```bash
pipenv run scraping
```

### Scraping
> Crea un nuevo archivo y con los 3 csv juntos (para simplificar importarlo para un motor de DB). El resultado se guarda en app/data/time_series_export.csv *pipenv install --dev (requererido)

```bash
pipenv run export
```

### Actualiza los archivos requirement

```bash
invoke generate-reqs
```

[Pipfile.lock](./Pipfile.lock) se actualiza automaticamente cuando haces `pipenv install`.



## Licencia

Ver [LICENSE.md](LICENSE.md) para la licencia
