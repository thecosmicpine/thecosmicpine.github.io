---
layout: default
title: Notes
nav_order: 5
permalink: /notes/
---

# Notes 글 목록

`categories`에 `Notes`가 들어간 글만 여기에 모입니다.

{% assign posts = site.categories.Notes %}
{% if posts and posts.size > 0 %}
<ul>
{% for post in posts %}
  <li>
    <a href="{{ post.url | relative_url }}">{{ post.title | escape }}</a>
    <small>{{ post.date | date: "%Y-%m-%d" }}</small>
  </li>
{% endfor %}
</ul>
{% else %}
<p>아직 `Notes` 카테고리 글이 없습니다.</p>
{% endif %}
