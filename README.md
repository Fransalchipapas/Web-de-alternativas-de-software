# Alternativas de software

Buscás un programa y la web muestra con qué se puede reemplazar.

## Local

```bash
cp .env.example .env
uv sync
uv run python manage.py migrate
uv run python manage.py createsuperuser
uv run python manage.py runserver
```

- Sitio: http://127.0.0.1:8000/
- Admin: http://127.0.0.1:8000/admin/

Cargá empresas, categorías y productos desde el admin. En cada producto, el inline "Alternativas de este producto" es la lista que aparece al buscarlo. Ahí `alternativa` es el reemplazo y el producto que estás editando es el que se reemplaza.

## Render

Servicio web con Docker, contexto en la raíz del repo, más una base PostgreSQL.

Variables:

- `SECRET_KEY`
- `DEBUG=False`
- `DATABASE_URL` (la URL interna de Render)
- `ALLOWED_HOSTS` (el host `.onrender.com`)
- `CSRF_TRUSTED_ORIGINS` (`https://tu-servicio.onrender.com`)

El contenedor corre las migraciones, junta los estáticos y levanta Gunicorn. El puerto lo toma de `PORT`.
ANOTACIÓN= tener en cuenta que whitenoise.storage.CompressedStaticFilesStorage es una config para despligue en  render
## git pull origin main --allow-unrelated-histories
Nos sirvió para actualizar el LINCENSE 
nos abrio vim con el enlace del repo, ahora nada más -> esc -> escribir :wq -> enter

## dockerizado
deberia poder construirse con 
````text
    docker build -t alternativas .  -> costruirlo
    docker run -p 10000:10000 alternativas -> ejecutarlo
````
Antes de ir a render tirar en la carpeta del proyecto=
uv run python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# Render
Escogemos el titulo de proyecto y el servicio gratuito, despues 
Creamos la postgres db, ponemos el nombre el computo -> create database
En info, copiamos el internal database URL para la var de entorno
En new -> creamos un web service y seleccionamos el proyecto de github
        |-New Web Service = language: Docker, root directory: null si ya se paró en Dockerfile y manage.py
        |-Compute: 0
        |-Enviroment Variables= toda la config del .env
            