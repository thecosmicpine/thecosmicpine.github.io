---
layout: default
title: 홈
nav_order: 1
permalink: /
---

<section class="home-hero">
  <h1>지금 모두가 얘기하는 그거, 쉽게</h1>
  <p>AI 도구, 집 안의 기기, 계절마다 생기는 생활 속 궁금증을 공식 자료로 확인해 풀어 씁니다.</p>
</section>

{%- assign manuals = site.posts | where_exp: "p", "p.categories contains '생활 매뉴얼'" -%}
{%- if manuals.size > 0 %}
<h2 class="home-section">생활 매뉴얼 <a href="{{ '/discover/life-manual/' | relative_url }}">전체 보기 →</a></h2>
<div class="card-grid card-grid--compact">
{%- for p in manuals limit: 4 -%}{% include post-card.html post=p compact=true %}{%- endfor -%}
</div>
{%- endif %}

<h2 class="home-section">최근 글 <a href="{{ '/archive/' | relative_url }}">전체 글 →</a></h2>
<div class="card-grid">
{%- for p in site.posts limit: 12 -%}{% include post-card.html post=p %}{%- endfor -%}
</div>

<h2 class="home-section">연재</h2>
<ul class="series-list">
{%- assign series_groups = site.posts | where_exp: "p", "p.series" | group_by: "series" -%}
{%- for g in series_groups -%}
  {%- assign first = g.items | sort: "series_order" | first -%}
  <li><a href="{{ first.url | relative_url }}">{{ g.name }}</a> <small>{{ g.items.size }}편</small></li>
{%- endfor -%}
</ul>
