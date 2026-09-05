---
layout: default
title: 홈
nav_order: 1
permalink: /
---

# 안녕하세요!

Sungwoon Lee의 개인 블로그에 오신 것을 환영합니다.

이곳에서 개발, 기술, 그리고 일상의 생각들을 공유합니다.

## 최근 글

{% assign recent_posts = site.posts | slice: 0, 5 %}
{% for post in recent_posts %}
- [{{ post.title | escape }}]({{ post.url | relative_url }}) - {{ post.date | date: "%Y년 %m월 %d일" }}
{% endfor %}

[전체 글 보기 →](/archive/)
