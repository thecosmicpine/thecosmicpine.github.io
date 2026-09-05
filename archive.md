---
layout: page
title: 글모음
permalink: /archive/
---

## 전체 포스트

{% for post in site.posts %}
  <article>
    <h3>
      <a href="{{ post.url | relative_url }}">
        {{ post.title | escape }}
      </a>
    </h3>
    <p class="post-meta">
      <time datetime="{{ post.date | date_to_xmlschema }}">
        {{ post.date | date: "%Y년 %m월 %d일" }}
      </time>
      {% if post.categories.size > 0 %}
        • {{ post.categories | join: ", " }}
      {% endif %}
    </p>
    {% if post.excerpt %}
      <p>{{ post.excerpt | strip_html | truncatewords: 30 }}</p>
    {% endif %}
  </article>
  <hr>
{% endfor %}
