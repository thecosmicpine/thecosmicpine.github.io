---
layout: default
title: Grok Bot
nav_order: 6
permalink: /grok-bot/
---

# Grok Bot 글 목록

`categories`에 `Grok Bot`이 들어간 글만 여기에 모입니다.

{% assign posts = site.categories["Grok Bot"] %}
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
<p>아직 `Grok Bot` 카테고리 글이 없습니다.</p>
{% endif %}