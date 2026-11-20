from fastapi.testclient import TestClient

from pokemon_api.app import create_app


def test_built_site_is_served_at_the_root(tmp_path):
    (tmp_path / "index.html").write_text("<h1>Arène des types</h1>", encoding="utf-8")

    with TestClient(create_app(static_dir=tmp_path)) as client:
        page = client.get("/")
        options = client.get("/api/options")

    assert page.status_code == 200
    assert "Arène des types" in page.text
    assert options.status_code == 200            # le site ne masque pas /api


def test_api_still_works_before_the_first_build(tmp_path):
    missing = tmp_path / "dist"                  # « npm run build » pas encore lancé

    with TestClient(create_app(static_dir=missing)) as client:
        assert client.get("/").status_code == 404
        assert client.get("/api/options").status_code == 200