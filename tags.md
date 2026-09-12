---
layout: default
title: 태그
nav_exclude: true
permalink: /tags/
---

# 태그

글에 붙인 태그로 모아 봅니다. 사이드 메뉴 아래에도 같은 목록이 있습니다.

{% assign sorted_tags = site.tags | sort %}
{% if sorted_tags.size == 0 %}
<p>아직 태그가 없습니다.</p>
{% else %}
{% for tag in sorted_tags %}
{% assign tag_name = tag[0] %}
{% assign tag_posts = tag[1] %}
<h2 id="{{ tag_name | slugify }}">{{ tag_name }} <small>({{ tag_posts.size }})</small></h2>
<ul>
{% for post in tag_posts %}
  <li><a href="{{ post.url | relative_url }}">{{ post.title | escape }}</a>
    <small>{{ post.date | date: "%Y-%m-%d" }}</small></li>
{% endfor %}
</ul>
{% endfor %}
{% endif %}
