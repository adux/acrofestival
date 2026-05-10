from django.conf import settings
from django.db import models


class Teacher(models.Model):
    """A person who teaches at festivals. Reused across years."""

    name = models.CharField(max_length=200)
    country = models.CharField(max_length=100, blank=True)
    photo = models.ImageField(upload_to="teachers/", blank=True, null=True)
    bio = models.TextField(blank=True)
    instagram_url = models.URLField(blank=True)
    website_url = models.URLField(blank=True)
    notes = models.TextField(
        blank=True,
        help_text="Internal notes (not shown publicly).",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class TeacherAppearance(models.Model):
    """Assignment of a teacher to a specific festival edition."""

    teacher = models.ForeignKey(
        Teacher, on_delete=models.CASCADE, related_name="appearances"
    )
    festival_key = models.CharField(max_length=50)
    year = models.PositiveIntegerField()
    role_label = models.CharField(
        max_length=200,
        blank=True,
        help_text="Optional override of the team/instagram-handle line shown under the name.",
    )
    order = models.PositiveIntegerField(default=0)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["order", "id"]
        constraints = [
            models.UniqueConstraint(
                fields=["teacher", "festival_key", "year"],
                name="unique_teacher_per_festival_year",
            )
        ]
        indexes = [
            models.Index(fields=["festival_key", "year", "order"]),
        ]

    def __str__(self) -> str:
        return f"{self.teacher.name} @ {self.festival_key} {self.year}"


class ContentSnippet(models.Model):
    """Live override for a YAML-defined snippet key.

    Absence of a row means the YAML default is in effect.
    """

    key = models.CharField(max_length=200, unique=True)
    value = models.TextField(blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="+",
    )

    class Meta:
        ordering = ["key"]

    def __str__(self) -> str:
        return self.key


class ContentSnippetHistory(models.Model):
    """Append-only log of every save through the editor."""

    key = models.CharField(max_length=200, db_index=True)
    value = models.TextField(blank=True)
    edited_at = models.DateTimeField(auto_now_add=True)
    edited_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="+",
    )
    edited_by_name = models.CharField(max_length=200, blank=True)
    note = models.CharField(max_length=200, blank=True)

    class Meta:
        ordering = ["-edited_at"]
        indexes = [
            models.Index(fields=["key", "-edited_at"]),
        ]

    def __str__(self) -> str:
        return f"{self.key} @ {self.edited_at:%Y-%m-%d %H:%M}"
