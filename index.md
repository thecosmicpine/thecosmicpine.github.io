---
layout: default
title: 홈
nav_order: 1
permalink: /
---

## 최근 글

{% assign recent_posts = site.posts | slice: 0, 5 %}
{% for post in recent_posts %}
- [{{ post.title | escape }}]({{ post.url | relative_url }}) - {{ post.date | date: "%Y년 %m월 %d일" }}
{% endfor %}

[전체 글 보기 →](/archive/)
