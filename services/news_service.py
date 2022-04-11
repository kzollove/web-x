#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
:Mod: featured_service

:Synopsis:

:Author:
    servilla

:Created:
    4/5/22
"""
from pathlib import Path

import fastapi_chameleon
from bs4 import BeautifulSoup

from services.clipper import clip
from services.literal import Literal
from services.grid_object import GridObject


def get_html(name: str) -> Literal:
    template_path = fastapi_chameleon.engine.template_path
    featured_file = f"{template_path}/news/{name}.html"
    with Path(featured_file).open("r", encoding="utf-8") as f:
        html = f.read()
    return Literal(html)


def get_grid_objects() -> list:
    grid_objects = []
    template_path = fastapi_chameleon.engine.template_path
    news_path = f"{template_path}/news"
    if Path(news_path).is_dir():
        for obj in sorted(Path(news_path).rglob("news-*.*.html"), reverse=True):
            if obj.is_file():
                n = f"{news_path}/{obj.name}"
                go = make_grid_object(n)
                grid_objects.append(go)
    return grid_objects


def make_grid_object(file: str) -> GridObject:
    name = Path(file).stem
    fd = Path(file).open("r", encoding="utf-8").read()
    soup = BeautifulSoup(fd, "lxml")
    title = soup.find("h2").get_text()
    paras = soup.find_all("p")
    date = paras[0].get_text()
    author = paras[1].get_text()
    h3s = soup.find_all("h3")
    description = None
    for h3 in h3s:
        if h3.get_text() == "Description":
            description = h3.findNext("p").get_text()
    image = soup.find("img")
    thumbnail = None
    if image:
        thumbnail = image["src"]

    return GridObject(
        name=name,
        title=title,
        thumbnail=thumbnail,
        date=date,
        author=author,
        description=clip(description, 200)
    )
