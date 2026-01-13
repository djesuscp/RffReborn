import os
import hashlib
from collections import defaultdict
from typing import Callable
import threading

# --------------------------------------------------
# Configuración
# --------------------------------------------------

HASH_CHUNK_SIZE = 1024 * 1024  # 1 MB por bloque
PARTIAL_HASH_SIZE = 1024 * 1024  # 1 MB para hash parcial


# --------------------------------------------------
# Utilidades de hashing
# --------------------------------------------------

def _hash_file(path: str, *, partial: bool = False) -> str | None:
    """
    Calcula el hash de un archivo.
    - partial=True -> solo primeros PARTIAL_HASH_SIZE bytes
    - partial=False -> archivo completo
    """
    try:
        hasher = hashlib.sha256()
        with open(path, "rb") as f:
            if partial:
                hasher.update(f.read(PARTIAL_HASH_SIZE))
            else:
                while chunk := f.read(HASH_CHUNK_SIZE):
                    hasher.update(chunk)
        return hasher.hexdigest()
    except Exception:
        return None


# --------------------------------------------------
# Motor principal
# --------------------------------------------------

def scan_duplicates(
    root_path: str,
    *,
    progress_cb: Callable[[dict], None] | None = None,
    cancel_event: threading.Event | None = None
) -> list[dict]:
    """
    Escanea un directorio buscando archivos duplicados reales.
    """

    # ----------------------------------------------
    # FASE 0: contar archivos (para progreso real)
    # ----------------------------------------------

    total_files = 0
    processed_files = 0

    for root, _, files in os.walk(root_path):
        for _ in files:
            total_files += 1

    if progress_cb:
        progress_cb({
            "phase": "count",
            "total_files": total_files
        })


    # ----------------------------------------------
    # FASE 1: recorrer archivos y agrupar por tamaño
    # ----------------------------------------------

    size_buckets: dict[int, list[str]] = defaultdict(list)
    scanned_files = 0

    for root, _, files in os.walk(root_path):
        for file in files:

            if cancel_event and cancel_event.is_set():
                return []

            path = os.path.join(root, file)

            try:
                size = os.path.getsize(path)
            except OSError:
                continue

            size_buckets[size].append(path)
            scanned_files += 1
            
            processed_files += 1

            if progress_cb:
                progress_cb({
                    "phase": "scan",
                    "current": path,
                    "processed": processed_files,
                    "total": total_files
                })

            if progress_cb:
                progress_cb({
                    "phase": "scan",
                    "current": path,
                    "files_scanned": scanned_files
                })

    # Solo tamaños con más de un archivo
    size_groups = [
        group for group in size_buckets.values()
        if len(group) > 1
    ]

    # ----------------------------------------------
    # FASE 2: hash parcial
    # ----------------------------------------------

    partial_buckets: dict[tuple[int, str], list[str]] = defaultdict(list)

    for group in size_groups:
        for path in group:

            if cancel_event and cancel_event.is_set():
                return []

            partial_hash = _hash_file(path, partial=True)
            if not partial_hash:
                continue

            key = (os.path.getsize(path), partial_hash)
            partial_buckets[key].append(path)
            
            processed_files += 1

            if progress_cb:
                progress_cb({
                    "phase": "scan",
                    "current": path,
                    "processed": processed_files,
                    "total": total_files
                })

            if progress_cb:
                progress_cb({
                    "phase": "partial-hash",
                    "current": path
                })

    partial_groups = [
        group for group in partial_buckets.values()
        if len(group) > 1
    ]

    # ----------------------------------------------
    # FASE 3: hash completo (confirmación)
    # ----------------------------------------------

    full_buckets: dict[str, list[str]] = defaultdict(list)

    for group in partial_groups:
        for path in group:

            if cancel_event and cancel_event.is_set():
                return []

            full_hash = _hash_file(path, partial=False)
            if not full_hash:
                continue

            full_buckets[full_hash].append(path)

            processed_files += 1

            if progress_cb:
                progress_cb({
                    "phase": "scan",
                    "current": path,
                    "processed": processed_files,
                    "total": total_files
                })

            if progress_cb:
                progress_cb({
                    "phase": "full-hash",
                    "current": path
                })

    # ----------------------------------------------
    # RESULTADO FINAL
    # ----------------------------------------------

    results = []

    for h, files in full_buckets.items():
        if len(files) > 1:
            try:
                size = os.path.getsize(files[0])
            except OSError:
                size = 0

            results.append({
                "hash": h,
                "size": size,
                "files": files
            })

    return results
