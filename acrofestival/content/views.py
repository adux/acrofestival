from datetime import date
from typing import Dict

from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.db import transaction
from django.db.models import Max
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_http_methods

from acrofestival.content.forms import TeacherForm
from acrofestival.content.models import (
    ContentSnippet,
    ContentSnippetHistory,
    Teacher,
    TeacherAppearance,
)
from acrofestival.content.snippets import ContentSnippets


FESTIVALS = [
    {"key": "urbanacro", "name": "Urban Acro Festival", "file": "urbanacro.yml"},
    {"key": "winteracro", "name": "Winter Acro Festival", "file": "winteracro.yml"},
    {"key": "dap", "name": "Dynamic Acro Program", "file": "dap.yml"},
    {"key": "general", "name": "General Content", "file": "general.yml"},
]
FESTIVALS_BY_KEY = {f["key"]: f for f in FESTIVALS}


def _user_display_name(user) -> str:
    return user.get_full_name() or user.get_username()


def _yaml_defaults_for(festival_key: str) -> Dict[str, str]:
    festival = FESTIVALS_BY_KEY[festival_key]
    snippets = ContentSnippets()
    keys = snippets.yaml_keys_for_files([festival["file"]])
    return {key: snippets.yaml_default(key) for key in keys}


@staff_member_required
@require_http_methods(["GET"])
def content_editor_list(request):
    return render(request, "content/editor_list.html", {"festivals": FESTIVALS})


@staff_member_required
@require_http_methods(["GET", "POST"])
def content_editor_edit(request, festival):
    if festival not in FESTIVALS_BY_KEY:
        messages.error(request, f"Festival '{festival}' not found")
        return redirect("content:editor_list")

    yaml_defaults = _yaml_defaults_for(festival)
    overrides = {
        s.key: s
        for s in ContentSnippet.objects.filter(key__in=yaml_defaults.keys())
    }

    if request.method == "POST":
        changed = 0
        with transaction.atomic():
            for key, default_value in yaml_defaults.items():
                field_name = f"content_{key}"
                if field_name not in request.POST:
                    # Field wasn't submitted at all — leave as-is to avoid
                    # accidental deletion from a partial form post.
                    continue
                posted = request.POST[field_name]
                current = overrides[key].value if key in overrides else default_value

                if posted == current:
                    continue

                if posted == default_value and key in overrides:
                    overrides[key].delete()
                else:
                    ContentSnippet.objects.update_or_create(
                        key=key,
                        defaults={"value": posted, "updated_by": request.user},
                    )

                ContentSnippetHistory.objects.create(
                    key=key,
                    value=posted,
                    edited_by=request.user,
                    edited_by_name=_user_display_name(request.user),
                )
                changed += 1

        if changed:
            ContentSnippets.bump_version()
            messages.success(request, f"Saved {changed} change(s)")
        else:
            messages.info(request, "No changes to save")
        return redirect("content:editor_edit", festival=festival)

    rows = []
    for key, default_value in sorted(yaml_defaults.items()):
        override = overrides.get(key)
        rows.append({
            "key": key,
            "value": override.value if override else default_value,
            "default_value": default_value,
            "is_overridden": override is not None,
            "updated_at": override.updated_at if override else None,
            "updated_by": _user_display_name(override.updated_by) if override and override.updated_by else "",
        })

    return render(request, "content/editor_edit.html", {
        "festival": festival,
        "festival_name": FESTIVALS_BY_KEY[festival]["name"],
        "rows": rows,
    })


@staff_member_required
@require_http_methods(["POST"])
def content_editor_reset(request, festival, key):
    if festival not in FESTIVALS_BY_KEY:
        messages.error(request, f"Festival '{festival}' not found")
        return redirect("content:editor_list")

    yaml_defaults = _yaml_defaults_for(festival)
    if key not in yaml_defaults:
        messages.error(request, f"Key '{key}' is not part of {festival}")
        return redirect("content:editor_edit", festival=festival)

    deleted, _ = ContentSnippet.objects.filter(key=key).delete()
    if deleted:
        ContentSnippetHistory.objects.create(
            key=key,
            value=yaml_defaults[key],
            edited_by=request.user,
            edited_by_name=_user_display_name(request.user),
            note="reset to default",
        )
        ContentSnippets.bump_version()
        messages.success(request, f"Reset '{key}' to default")
    else:
        messages.info(request, f"'{key}' was already at default")

    return redirect("content:editor_edit", festival=festival)


@staff_member_required
@require_http_methods(["GET"])
def content_editor_history(request, festival, key=None):
    if festival not in FESTIVALS_BY_KEY:
        messages.error(request, f"Festival '{festival}' not found")
        return redirect("content:editor_list")

    yaml_defaults = _yaml_defaults_for(festival)
    qs = ContentSnippetHistory.objects.filter(key__in=yaml_defaults.keys())
    if key:
        if key not in yaml_defaults:
            messages.error(request, f"Key '{key}' is not part of {festival}")
            return redirect("content:editor_history", festival=festival)
        qs = qs.filter(key=key)

    return render(request, "content/history.html", {
        "festival": festival,
        "festival_name": FESTIVALS_BY_KEY[festival]["name"],
        "filtered_key": key,
        "history": qs[:200],
    })


@staff_member_required
@require_http_methods(["POST"])
def content_editor_restore(request, history_id):
    entry = get_object_or_404(ContentSnippetHistory, pk=history_id)
    festival = request.POST.get("festival", "")

    with transaction.atomic():
        ContentSnippet.objects.update_or_create(
            key=entry.key,
            defaults={"value": entry.value, "updated_by": request.user},
        )
        ContentSnippetHistory.objects.create(
            key=entry.key,
            value=entry.value,
            edited_by=request.user,
            edited_by_name=_user_display_name(request.user),
            note=f"restored from {entry.edited_at:%Y-%m-%d %H:%M}",
        )
    ContentSnippets.bump_version()
    messages.success(
        request,
        f"Restored '{entry.key}' to value from {entry.edited_at:%Y-%m-%d %H:%M}",
    )

    if festival in FESTIVALS_BY_KEY:
        return redirect("content:editor_edit", festival=festival)
    return redirect("content:editor_list")


# ---------------------------------------------------------------------------
# Teachers
# ---------------------------------------------------------------------------


YEAR_SNIPPET_KEYS = {
    "urbanacro": "urbanacro_teachers_year",
    "winteracro": "winteracro_teachers_year",
    "dap": "dap_teachers_year",
}


def _default_year_for(festival: str) -> int:
    """Pick the year shown on the public site (snippet-driven), with fallbacks."""
    snippet_key = YEAR_SNIPPET_KEYS.get(festival)
    if snippet_key:
        raw = ContentSnippets().get_snippet(snippet_key, "")
        if raw.isdigit():
            return int(raw)
    latest = (
        TeacherAppearance.objects.filter(festival_key=festival)
        .aggregate(y=Max("year"))["y"]
    )
    return latest or date.today().year


def _resolve_year(request, festival: str) -> int:
    raw = request.GET.get("year") or request.POST.get("year")
    if raw and raw.isdigit():
        return int(raw)
    return _default_year_for(festival)


def _available_years(festival: str, current_year: int):
    years = set(
        TeacherAppearance.objects.filter(festival_key=festival)
        .values_list("year", flat=True)
    )
    years.add(current_year)
    return sorted(years, reverse=True)


@staff_member_required
@require_http_methods(["GET"])
def teachers_list(request, festival):
    if festival not in FESTIVALS_BY_KEY:
        messages.error(request, f"Festival '{festival}' not found")
        return redirect("content:editor_list")

    year = _resolve_year(request, festival)
    appearances = (
        TeacherAppearance.objects.filter(festival_key=festival, year=year)
        .select_related("teacher")
        .order_by("order", "id")
    )
    assigned_teacher_ids = appearances.values_list("teacher_id", flat=True)
    candidates = Teacher.objects.exclude(id__in=assigned_teacher_ids).order_by("name")

    return render(request, "content/teachers_list.html", {
        "festival": festival,
        "festival_name": FESTIVALS_BY_KEY[festival]["name"],
        "year": year,
        "years": _available_years(festival, year),
        "appearances": appearances,
        "candidates": candidates,
    })


@staff_member_required
@require_http_methods(["GET", "POST"])
def teacher_create(request, festival):
    if festival not in FESTIVALS_BY_KEY:
        messages.error(request, f"Festival '{festival}' not found")
        return redirect("content:editor_list")

    year = _resolve_year(request, festival)

    if request.method == "POST":
        form = TeacherForm(request.POST, request.FILES)
        if form.is_valid():
            with transaction.atomic():
                teacher = form.save()
                next_order = (
                    TeacherAppearance.objects
                    .filter(festival_key=festival, year=year)
                    .aggregate(m=Max("order"))["m"] or 0
                ) + 1
                TeacherAppearance.objects.create(
                    teacher=teacher,
                    festival_key=festival,
                    year=year,
                    order=next_order,
                )
            messages.success(request, f"Created '{teacher.name}' and added to {year}")
            return _redirect_to_teachers(festival, year)
    else:
        form = TeacherForm()

    return render(request, "content/teacher_form.html", {
        "festival": festival,
        "festival_name": FESTIVALS_BY_KEY[festival]["name"],
        "year": year,
        "form": form,
        "teacher": None,
    })


@staff_member_required
@require_http_methods(["GET", "POST"])
def teacher_edit(request, festival, teacher_id):
    if festival not in FESTIVALS_BY_KEY:
        messages.error(request, f"Festival '{festival}' not found")
        return redirect("content:editor_list")

    teacher = get_object_or_404(Teacher, pk=teacher_id)
    year = _resolve_year(request, festival)

    if request.method == "POST":
        form = TeacherForm(request.POST, request.FILES, instance=teacher)
        if form.is_valid():
            form.save()
            messages.success(request, f"Updated '{teacher.name}'")
            return _redirect_to_teachers(festival, year)
    else:
        form = TeacherForm(instance=teacher)

    return render(request, "content/teacher_form.html", {
        "festival": festival,
        "festival_name": FESTIVALS_BY_KEY[festival]["name"],
        "year": year,
        "form": form,
        "teacher": teacher,
        "teacher_appearances": teacher.appearances.order_by("-year"),
    })


@staff_member_required
@require_http_methods(["POST"])
def appearance_add(request, festival):
    if festival not in FESTIVALS_BY_KEY:
        messages.error(request, f"Festival '{festival}' not found")
        return redirect("content:editor_list")

    year = _resolve_year(request, festival)
    teacher_id = request.POST.get("teacher_id")
    if not teacher_id:
        messages.error(request, "No teacher selected")
        return _redirect_to_teachers(festival, year)

    teacher = get_object_or_404(Teacher, pk=teacher_id)
    next_order = (
        TeacherAppearance.objects
        .filter(festival_key=festival, year=year)
        .aggregate(m=Max("order"))["m"] or 0
    ) + 1
    _, created = TeacherAppearance.objects.get_or_create(
        teacher=teacher,
        festival_key=festival,
        year=year,
        defaults={"order": next_order},
    )
    if created:
        messages.success(request, f"Added '{teacher.name}' to {year}")
    else:
        messages.info(request, f"'{teacher.name}' is already in {year}")
    return redirect(f"{request_url(festival)}?year={year}")


@staff_member_required
@require_http_methods(["POST"])
def appearance_remove(request, appearance_id):
    appearance = get_object_or_404(TeacherAppearance, pk=appearance_id)
    festival = appearance.festival_key
    year = appearance.year
    name = appearance.teacher.name
    appearance.delete()
    messages.success(request, f"Removed '{name}' from {year}")
    if festival in FESTIVALS_BY_KEY:
        return _redirect_to_teachers(festival, year)
    return redirect("content:editor_list")


@staff_member_required
@require_http_methods(["POST"])
def appearance_move(request, appearance_id, direction):
    appearance = get_object_or_404(TeacherAppearance, pk=appearance_id)
    festival = appearance.festival_key
    year = appearance.year

    siblings = list(
        TeacherAppearance.objects
        .filter(festival_key=festival, year=year)
        .order_by("order", "id")
    )
    try:
        idx = next(i for i, a in enumerate(siblings) if a.id == appearance.id)
    except StopIteration:
        return _redirect_to_teachers(festival, year)

    swap_idx = idx - 1 if direction == "up" else idx + 1
    if 0 <= swap_idx < len(siblings):
        a, b = appearance, siblings[swap_idx]
        with transaction.atomic():
            # Two-step swap to avoid hitting the unique-by-order if we ever add it.
            a.order, b.order = b.order, a.order
            a.save(update_fields=["order"])
            b.save(update_fields=["order"])

    if festival in FESTIVALS_BY_KEY:
        return _redirect_to_teachers(festival, year)
    return redirect("content:editor_list")


@staff_member_required
@require_http_methods(["POST"])
def appearance_toggle_published(request, appearance_id):
    appearance = get_object_or_404(TeacherAppearance, pk=appearance_id)
    appearance.is_published = not appearance.is_published
    appearance.save(update_fields=["is_published"])
    festival = appearance.festival_key
    year = appearance.year
    if festival in FESTIVALS_BY_KEY:
        return _redirect_to_teachers(festival, year)
    return redirect("content:editor_list")


def _redirect_to_teachers(festival: str, year: int) -> HttpResponseRedirect:
    return HttpResponseRedirect(
        reverse("content:teachers_list", args=[festival]) + f"?year={year}"
    )
