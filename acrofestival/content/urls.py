from django.urls import path

from acrofestival.content import views

app_name = "content"

urlpatterns = [
    path("", views.content_editor_list, name="editor_list"),
    path(
        "history/restore/<int:history_id>/",
        views.content_editor_restore,
        name="editor_restore",
    ),
    path("<str:festival>/", views.content_editor_edit, name="editor_edit"),
    path(
        "<str:festival>/reset/<str:key>/",
        views.content_editor_reset,
        name="editor_reset",
    ),
    path(
        "<str:festival>/history/",
        views.content_editor_history,
        name="editor_history",
    ),
    path(
        "<str:festival>/history/<str:key>/",
        views.content_editor_history,
        name="editor_history_key",
    ),
    path(
        "<str:festival>/teachers/",
        views.teachers_list,
        name="teachers_list",
    ),
    path(
        "<str:festival>/teachers/new/",
        views.teacher_create,
        name="teacher_create",
    ),
    path(
        "<str:festival>/teachers/<int:teacher_id>/edit/",
        views.teacher_edit,
        name="teacher_edit",
    ),
    path(
        "<str:festival>/teachers/add-existing/",
        views.appearance_add,
        name="appearance_add",
    ),
    path(
        "appearances/<int:appearance_id>/remove/",
        views.appearance_remove,
        name="appearance_remove",
    ),
    path(
        "appearances/<int:appearance_id>/move/<str:direction>/",
        views.appearance_move,
        name="appearance_move",
    ),
    path(
        "appearances/<int:appearance_id>/toggle-published/",
        views.appearance_toggle_published,
        name="appearance_toggle_published",
    ),
]
