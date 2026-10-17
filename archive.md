---
layout: default
title: 글모음
nav_order: 2
permalink: /archive/
---

# 전체 글 <small>({{ site.posts.size }})</small>

{%- assign by_month = site.posts | group_by_exp: "p", "p.date | date: '%Y년 %-m월'" -%}
{%- for m in by_month %}
<h2 class="archive-month">{{ m.name }} <small>({{ m.items.size }})</small></h2>
<ul class="archive-list">
{%- for p in m.items -%}
  <li><span class="archive-date">{{ p.date | date: "%m.%d" }}</span> <a href="{{ p.url | relative_url }}">{{ p.title | escape }}</a> <small class="archive-cat">{{ p.categories | first }}</small></li>
{%- endfor -%}
</ul>
{%- endfor %}
