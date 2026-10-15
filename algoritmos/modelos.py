"""Tipos compartidos para datos estructurados de los algoritmos."""

from dataclasses import dataclass


@dataclass(frozen=True)
class PasoProcedimiento:
    titulo: str
    explicacion: str
    encabezados: tuple[str, ...]
    filas: tuple[tuple[str, ...], ...]
