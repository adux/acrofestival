from django.contrib.sitemaps import Sitemap
from django.urls import reverse


class StaticViewSitemap(Sitemap):
    """Sitemap entries for all public, indexable pages.

    Tuples: (url_name, priority, changefreq).
    Registration form is excluded — it's `noindex` on the template anyway.
    """

    _entries = [
        ("home", 1.0, "weekly"),
        ("urbanacro", 0.9, "weekly"),
        ("winteracro", 0.9, "weekly"),
        ("dap", 0.9, "monthly"),
        ("winterlocation", 0.7, "monthly"),
        ("winteraccommodation", 0.7, "monthly"),
        ("winterconditions", 0.7, "monthly"),
        ("pictures", 0.6, "monthly"),
    ]

    def items(self):
        return self._entries

    def location(self, item):
        return reverse(item[0])

    def priority(self, item):
        return item[1]

    def changefreq(self, item):
        return item[2]
