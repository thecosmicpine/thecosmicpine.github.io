---
layout: page
title: "dev 폴더"
permalink: /dev/
---

## `/dev/` 글 목록 샘플

GitHub Pages(Jekyll)에서는 `_posts/dev/` 폴더만으로 목록 URL이 생기지 않습니다.
대신 **같은 이름 카테고리**(`categories: [dev]`) 글을 이 페이지에서 모아 보여줍니다.

{% assign posts = site.categories.dev %}
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
<p>아직 `dev` 카테고리 글이 없습니다.</p>
{% endif %}

---

파일 위치 예시: `_posts/dev/YYYY-MM-DD-title.md` + front matter에 `categories: [dev]`
