"""Convención provisional: domingo a sábado, semana 1 contiene el 4 de enero.

Compartida con la exploración NASA. NO certifica equivalencia con el calendario
MINSA de todos los años. Las etiquetas incompatibles se conservan para revisión.
"""
from datetime import date, timedelta
from operator import index


def year_start(year: int) -> date:
    year = index(year)
    january4 = date(year, 1, 4)
    return january4 - timedelta(days=(january4.weekday() + 1) % 7)


def weeks_in_year(year: int) -> int:
    return (year_start(year + 1) - year_start(year)).days // 7


def week_start(year: int, week: int) -> date:
    year, week = index(year), index(week)
    if not 1 <= week <= weeks_in_year(year):
        raise ValueError(f"Semana incompatible con la convención provisional: {year}-{week}")
    return year_start(year) + timedelta(weeks=week - 1)


def epi_week(day: date) -> tuple[int, int]:
    year = day.year
    if day < year_start(year):
        year -= 1
    elif day >= year_start(year + 1):
        year += 1
    return year, (day - year_start(year)).days // 7 + 1
