---
layout: default
title: 글모음
nav_order: 3
permalink: /archive/
---

# 전체 포스트

{% for post in site.posts %}
## [{{ post.title | escape }}]({{ post.url | relative_url }})

**{{ post.date | date: "%Y년 %m월 %d일" }}**{% if post.categories.size > 0 %} • {{ post.categories | join: ", " }}{% endif %}

{% if post.excerpt %}
{{ post.excerpt | strip_html | truncatewords: 30 }}
{% endif %}

---

{% endfor %}
