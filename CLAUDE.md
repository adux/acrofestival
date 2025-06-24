# Acro Festival Project - Claude Development Notes

## Project Overview

This Django project manages three distinct acrobatics festival websites using a shared codebase:

1. **Urban Acro Festival** (urbanacro) - Summer festival in Zürich, August 16-18, 2024
2. **Winter Acro Festival** (winteracro) - Winter festival in Arosa, February 22 - March 1, 2025  
3. **DAP (Dynamic Acro Program)** (dap) - 21-day intensive acro program

## Content Management Migration

### Current State
- **Legacy System**: django-tinycontent (database-stored content)
- **New System**: Custom YAML-based content system in `acrofestival.content` app
- **Status**: Both systems exist, migration in progress

### Migration Strategy: Tinycontent → Custom Content System

#### Phase 1: Urban Acro Migration (CURRENT)
**Objective**: Replace tinycontent usage in Urban Acro Festival templates

**Templates to migrate**:
- `/acrofestival/templates/frontpage.html` (urban content only)
- `/acrofestival/templates/pages/urbanacro/home.html` (main template)

**Content keys for Urban Acro**:
- `urban_general_date` (used multiple times)
- `urban_general_version` 
- `urban_general_description`
- `urban_general_participants`
- `urbanacro_general_workshops`
- `urban_general_included`
- `urban_general_food`
- `urban_general_sleeping`
- `urbanacro_teachers_year`
- `urbanacro_teachers_about`
- Teacher-specific keys: `urbanacro_teachers_teacher1_*`, `urbanacro_teachers_teacher2_*`, `urbanacro_teachers_teacher3_*`

#### Phase 2: Winter Acro Migration (PLANNED)
**Templates to migrate**:
- `/acrofestival/templates/pages/winteracro/index.html`
- `/acrofestival/templates/pages/winteracro/accommodation.html`
- `/acrofestival/templates/pages/winteracro/location.html`
- `/acrofestival/templates/pages/winteracro/conditions.html`
- `/acrofestival/templates/pages/winteracro/pictures.html`
- `/acrofestival/templates/pages/formulario/homeform.html`
- `/acrofestival/templates/snippets/footer.html`

#### Phase 3: Cleanup (PLANNED)
- Remove tinycontent from INSTALLED_APPS
- Remove tinycontent references
- Database cleanup

### Content System Architecture

#### YAML Content Location
- **Main file**: `/config/snippets/snippets.yml`
- **Environment-specific**: `/config/snippets/snippets_<env>.yml` (optional)
- **Environment detection**: `DJANGO_ENV` environment variable

#### Template Tag Usage
**Old (tinycontent)**:
```html
{% load tinycontent_tags %}
{% tinycontent_simple 'key_name' %}
```

**New (custom content)**:
```html
{% load content_tags %}
{% content_snippet 'key_name' %}
```

#### Content Management Class
- **Location**: `/acrofestival/content/snippets.py`
- **Class**: `ContentSnippets` (singleton pattern)
- **Features**: Auto-reload, environment-specific files, default values

## Migration Progress Tracker

### ✅ Completed
- [x] Created custom content app
- [x] Added app to INSTALLED_APPS
- [x] Created template tags system
- [x] Converted JSON content to YAML format
- [x] Analysis of current tinycontent usage

### 🔄 In Progress
- [ ] **Urban Acro Migration** (Phase 1)
  - [ ] Update frontpage.html (urban content only)
  - [ ] Update urbanacro/home.html template
  - [ ] Test urban acro website functionality
  - [ ] Verify all content displays correctly

### 📋 Planned
- [ ] **Winter Acro Migration** (Phase 2)
  - [ ] Update winteracro templates (6 templates)
  - [ ] Update registration form template
  - [ ] Update footer snippet
  - [ ] Test winter acro website functionality
- [ ] **System Cleanup** (Phase 3)
  - [ ] Remove tinycontent from INSTALLED_APPS
  - [ ] Remove tinycontent_export.json
  - [ ] Database cleanup
  - [ ] Final testing across all websites

## URL Structure

```
/ → Frontpage (links to all festivals)
/urbanacro/ → Urban Acro Festival home
/winteracro/ → Winter Acro Festival home
  /winteracro/form/ → Registration form
  /winteracro/location → Location details
  /winteracro/accommodation → Accommodation options  
  /winteracro/conditions → Pricing and conditions
/pictures/ → Winter festival pictures
/dap/ → Dynamic Acro Program
```

## Development Commands

### Run Development Server
```bash
python manage.py runserver
```

### Test Specific Website
```bash
# Urban Acro
curl http://localhost:8000/urbanacro/

# Winter Acro  
curl http://localhost:8000/winteracro/

# DAP
curl http://localhost:8000/dap/
```

### Content Management
```bash
# Reload content (if needed)
python manage.py shell
>>> from acrofestival.content.snippets import ContentSnippets
>>> ContentSnippets().reload()
```

## Important Notes

- **Three distinct websites** run from the same Django project
- **Content is environment-aware** (development/production YAML files)
- **Existing tinycontent data** has been exported and converted to YAML
- **Migration must be done carefully** to avoid breaking live websites
- **Test each website independently** after migration steps