# Acro Festival Project

Django project running three festival websites from a shared codebase:

1. **Urban Acro Festival** (urbanacro) — summer festival in Zürich
2. **Winter Acro Festival** (winteracro) — winter festival in Arosa
3. **DAP (Dynamic Acro Program)** (dap) — multi-week intensive program

Annual dates change every year and live in YAML / DB content (see below), not in this doc.

## Apps

| App | Path | Purpose |
|---|---|---|
| `acrofestival.users` | `acrofestival/users/` | Custom user model + allauth integration |
| `acrofestival.booking` | `acrofestival/booking/` | Urban + Winter registration models, forms, views |
| `acrofestival.winteracro` | `acrofestival/winteracro/` | Winter site views + workshop/teacher models |
| `acrofestival.dap` | `acrofestival/dap/` | DAP page view |
| `acrofestival.content` | `acrofestival/content/` | YAML+DB content snippets, urbanacro Teacher model, web editor |

## Content system

Three layers, in priority order on read:

1. **`ContentSnippet` rows** (DB) — overrides edited via the web editor.
2. **YAML defaults** in `config/snippets/*.yml` — committed to git, edited by devs.
3. **Caller fallback** — the optional second arg to `{% content_snippet 'key' 'fallback' %}`.

Files loaded in order (later overrides earlier): `general.yml` → `winteracro.yml` → `urbanacro.yml` → `dap.yml` → `snippets.yml` → `snippets_<DJANGO_ENV>.yml`.

The merged dict is cached in Django's cache framework (Redis in prod, locmem in dev) under a versioned key. `ContentSnippets.bump_version()` is called by every save in the editor — all gunicorn workers see the new value on next request.

### Template tag

```django
{% load content_tags %}
{% content_snippet 'urban_general_title' %}
{% content_snippet 'some_key' 'optional fallback' %}
```

Output is `mark_safe`d, so HTML in YAML/DB values renders as HTML.

### Web editor

`/content-editor/` (staff-only):

- `/content-editor/<festival>/` — flat list of all keys for that festival, with badges for *default* vs *overridden*, per-key reset-to-default, and per-key history link.
- `/content-editor/<festival>/history/` — last 200 changes, with restore.
- `/content-editor/urbanacro/teachers/` — teacher manager (see below).

Saves go straight to `ContentSnippet` / `ContentSnippetHistory`. No filesystem writes; no GitHub commits.

### Urbanacro teachers

Teachers are not snippets — they're rows in `Teacher` + `TeacherAppearance`:

- `Teacher` — name, country, photo (ImageField → S3 in prod), bio, instagram_url, website_url, notes. Reused across years.
- `TeacherAppearance` — `(teacher, festival_key, year, order, is_published, role_label)`.

The public year shown on `/urbanacro/` is driven by the `urbanacro_teachers_year` snippet. The view (`booking.views.urbanacro_view`) queries appearances for that year and passes them to the template. Recycle a teacher across years via the editor's "Add existing teacher" picker.

## URL structure

```
/                       → Frontpage (links to all festivals)
/urbanacro/             → Urban Acro Festival home
/winteracro/            → Winter Acro Festival home
  /winteracro/form/         → Registration form
  /winteracro/location      → Location details
  /winteracro/accommodation → Accommodation options
  /winteracro/conditions    → Pricing and conditions
/pictures/              → Winter festival pictures
/dap/                   → Dynamic Acro Program
/content-editor/        → Staff-only content editor
/admin/                 → Django admin
```

## Static files

- `STATICFILES_DIRS = [acrofestival/static]`. Urbanacro is the de-facto global theme — base.html pulls all CSS/JS/fonts from `static/urbanacro/`.
- Local dev: Django serves staticfiles directly via finders.
- Production: WhiteNoise (`CompressedManifestStaticFilesStorage`) + `manage.py collectstatic` writes hashed assets to `staticfiles/`.

Media (uploads) go to S3 in prod via `django-storages`, fronted by CloudFront (`AWS_S3_CUSTOM_DOMAIN`). Locally they land in `acrofestival/media/`.

## Development commands

```bash
# Run server
DJANGO_SETTINGS_MODULE=config.settings.local pipenv run python manage.py runserver

# Smoke-check each site
curl http://localhost:8000/urbanacro/
curl http://localhost:8000/winteracro/
curl http://localhost:8000/dap/

# Force-reload YAML defaults + invalidate content cache (rarely needed; deploys do it)
pipenv run python manage.py shell -c "from acrofestival.content.snippets import ContentSnippets; ContentSnippets().reload()"
```

## Deployment

Heroku + gunicorn (see `Procfile`). Release phase runs `manage.py migrate` automatically. Static files are picked up by WhiteNoise on each deploy; no separate `collectstatic` step in the Procfile (Heroku's Python buildpack runs it).
