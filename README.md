# API de biblioteca

Trabajo practico de FastAPI y SQLModel. Gestiona autores, libros, socios y prestamos con SQLite.

## Como correr

Se necesita Python 3.11 o posterior. Desde la carpeta del proyecto, en PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m uvicorn main:app --reload
```

Swagger queda en http://127.0.0.1:8000/docs. La base `biblioteca.db` se crea junto a `main.py`.
Para detener el servidor, usar Ctrl+C. Si el entorno ya existe, alcanza con activarlo.

## Como testear

```powershell
python -m pytest
```

Los tests de la API usan SQLite en memoria y una base nueva por prueba. Las pruebas de
concurrencia usan un archivo temporal, porque necesitan conexiones independientes. Los datos
de `biblioteca.db` no se usan en los tests. El comando informa la cobertura y falla si es menor
al 80 %. Para obtener un informe navegable:

```powershell
python -m pytest --cov-report=html
```

## Estructura

- `models/`: tablas y formatos de entrada y salida.
- `repositories/`: consultas y operaciones de guardado.
- `services/`: reglas de negocio y confirmacion de las transacciones.
- `routers/`: endpoints HTTP.
- `tests/`: CRUD, reglas de negocio, errores y transacciones.
- `database.py`: conexion, sesiones y creacion de tablas.
- `main.py`: inicio y registro de routers.

## Endpoints

| Metodo | Ruta | Uso |
| --- | --- | --- |
| POST / GET | `/autores/`, `/libros/`, `/socios/` | Crear o listar |
| GET / PATCH / DELETE | `/autores/{id}`, `/libros/{id}`, `/socios/{id}` | Consultar, modificar o eliminar |
| POST | `/libros/{id}/autores/{autor_id}` | Asociar un autor existente |
| GET | `/libros/?disponibles=true` | Listar libros con stock positivo |
| POST | `/prestamos/` | Prestar un libro |
| POST | `/prestamos/{id}/devolucion` | Devolver un prestamo |
| GET | `/socios/{id}/prestamos?activos=true` | Consultar prestamos activos |

Las rutas de colecciones tienen barra final. FastAPI redirige automaticamente si se omite.
Sin `activos=true`, la consulta del socio devuelve todo su historial.

## Ejemplo para probar en Swagger

Crear un autor con `{"nombre": "Borges", "nacionalidad": "Argentina"}`.
Crear un libro con `{"titulo": "Ficciones", "isbn": "9788420633129", "stock": 2, "anio": 1944}`.
Crear un socio con `{"nombre": "Ana", "email": "ana@example.com", "activo": true}`.
Usar los identificadores de las respuestas para asociar autor y libro.
Registrar un prestamo enviando `{"socio_id": 1, "libro_id": 1}`, reemplazando los IDs
por los que devolvio la API. Devolverlo con el ID del prestamo.

## Reglas y respuestas

- Cada socio puede tener hasta tres prestamos activos. El cuarto devuelve 409.
- Prestar descuenta un ejemplar. Sin stock devuelve 409. Un socio inactivo recibe 403.
- Las fechas se calculan en el servidor. El vencimiento es 14 dias despues del prestamo.
- Devolver repone un ejemplar y cobra 100 por dia de atraso, con un minimo de cero.
- Una segunda devolucion devuelve 409 y conserva el stock.
- Recursos inexistentes devuelven 404. ISBN o email repetidos devuelven 409.
- Stock negativo, email invalido y datos de entrada invalidos devuelven 422.
- Crear devuelve 201, consultar/modificar/devolver 200 y eliminar 204 sin cuerpo.

Las operaciones de prestamo y devolucion son transacciones completas. En SQLite se reserva
la escritura antes de comprobar el stock y los prestamos activos, para coordinar peticiones
simultaneas. No se permite eliminar libros o socios con prestamos registrados (409), incluso
si fueron devueltos, para conservar el historial. Eliminar un autor o un libro sin prestamos
elimina sus asociaciones de la tabla intermedia.

Las respuestas de libros incluyen `autores`. Los PATCH modifican solo los campos enviados
e ignoran valores `null`. Nacionalidad tiene valor inicial vacio y anio puede ser `null`
para admitir los registros creados en la primera version del proyecto. Ambos se pueden editar.
Al iniciar se agregan estas dos columnas si faltan, conservando los registros existentes.


