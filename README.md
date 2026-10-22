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