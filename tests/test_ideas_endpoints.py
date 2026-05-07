def test_create_and_get_idea(client):
    create = client.post("/ideas/new", json={"concept": "Build solar kiosks"})
    assert create.status_code == 201
    body = create.json()
    assert body["concept"] == "Build solar kiosks"
    assert "id" in body

    idea_id = body["id"]
    fetched = client.get(f"/ideas/{idea_id}")
    assert fetched.status_code == 200
    assert fetched.json()["id"] == idea_id


def test_get_all_ideas_sorted_by_score(client):
    a = client.post("/ideas/new", json={"concept": "Idea A"}).json()
    b = client.post("/ideas/new", json={"concept": "Idea B"}).json()

    # A gets +1 (up)
    r1 = client.post(f"/thumbs/{a['id']}/add_thumb", params={"new_thumb_type": "up"})
    assert r1.status_code == 200

    # B gets -1 (down)
    r2 = client.post(f"/thumbs/{b['id']}/add_thumb", params={"new_thumb_type": "down"})
    assert r2.status_code == 200

    all_ideas = client.get("/ideas")
    assert all_ideas.status_code == 200
    ids = [x["id"] for x in all_ideas.json()]

    assert ids.index(a["id"]) < ids.index(b["id"])
