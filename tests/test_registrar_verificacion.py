import json
import subprocess
import sys
from pathlib import Path

SCRIPT = Path("scripts/registrar_verificacion.py")


def _run(tmp_path, *args):
    textos = tmp_path / "normas_textos_literales.json"
    disciplinarias = tmp_path / "normas_disciplinarias.json"
    verif = tmp_path / "normas_verificaciones.json"

    textos.write_text(json.dumps({
        "LEY30057_ART94": {"texto_literal": "texto real de prueba"}
    }), encoding="utf-8")
    disciplinarias.write_text(json.dumps({
        "LEY30057_ART94": {"id": "LEY30057_ART94"}
    }), encoding="utf-8")

    src = SCRIPT.read_text(encoding="utf-8")
    src = src.replace('TEXTOS = Path("app/data/normas_textos_literales.json")',
                      f'TEXTOS = Path(r"{textos}")')
    src = src.replace('DISCIPLINARIAS = Path("app/data/normas_disciplinarias.json")',
                      f'DISCIPLINARIAS = Path(r"{disciplinarias}")')
    src = src.replace('VERIF = Path("app/data/normas_verificaciones.json")',
                      f'VERIF = Path(r"{verif}")')
    script_tmp = tmp_path / "script.py"
    script_tmp.write_text(src, encoding="utf-8")

    return subprocess.run(
        [sys.executable, str(script_tmp), *args],
        capture_output=True, text=True,
    ), verif


def test_url_sin_host_no_revienta(tmp_path):
    r, _ = _run(tmp_path, "LEY30057_ART94",
                "--url", "https://", "--fecha", "2026-10-20",
                "--por", "Israel Mercado", "--vigente", "si")
    assert r.returncode == 1
    assert "NO SE GUARDO NADA" in r.stdout


def test_id_inexistente_en_disciplinarias(tmp_path):
    r, _ = _run(tmp_path, "OTRO_ID",
                "--url", "https://www.gob.pe/algo-real",
                "--fecha", "2026-10-20",
                "--por", "Israel Mercado", "--vigente", "si")
    assert r.returncode == 1


def test_vigente_no_sin_derogada_por(tmp_path):
    r, _ = _run(tmp_path, "LEY30057_ART94",
                "--url", "https://www.gob.pe/algo-real",
                "--fecha", "2026-10-20",
                "--por", "Israel Mercado", "--vigente", "no")
    assert r.returncode == 1
    assert "derogada-por" in r.stdout


def test_derogada_por_inexistente(tmp_path):
    r, _ = _run(tmp_path, "LEY30057_ART94",
                "--url", "https://www.gob.pe/algo-real",
                "--fecha", "2026-10-20",
                "--por", "Israel Mercado", "--vigente", "no",
                "--derogada-por", "LEY_INEXISTENTE")
    assert r.returncode == 1


def test_modificacion_inexistente(tmp_path):
    r, _ = _run(tmp_path, "LEY30057_ART94",
                "--url", "https://www.gob.pe/algo-real",
                "--fecha", "2026-10-20",
                "--por", "Israel Mercado", "--vigente", "si",
                "--modificaciones", "LEY_FANTASMA")
    assert r.returncode == 1


def test_nombre_prohibido(tmp_path):
    r, _ = _run(tmp_path, "LEY30057_ART94",
                "--url", "https://www.gob.pe/algo-real",
                "--fecha", "2026-10-20",
                "--por", "admin", "--vigente", "si")
    assert r.returncode == 1


def test_reemplazar_deja_rastro(tmp_path):
    r1, verif = _run(tmp_path, "LEY30057_ART94",
                     "--url", "https://www.gob.pe/algo-real",
                     "--fecha", "2026-10-20",
                     "--por", "Israel Mercado", "--vigente", "si")
    assert r1.returncode == 0

    r2, verif = _run(tmp_path, "LEY30057_ART94",
                     "--url", "https://www.gob.pe/otra-real",
                     "--fecha", "2026-10-21",
                     "--por", "Israel Mercado", "--vigente", "si",
                     "--reemplazar")
    assert r2.returncode == 0
    datos = json.loads(verif.read_text(encoding="utf-8"))
    assert "_reemplaza_a" in datos["LEY30057_ART94"]
