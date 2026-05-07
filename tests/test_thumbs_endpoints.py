def test_thumbs_toggle_same_vote_removes_thumb(client):
    idea = client.post("/ideas/new", json={"concept": "Toggle test"}).json()
    idea_id = idea["id"]

    up_1 = client.post(f"/thumbs/{idea_id}/add_thumb", params={"new_thumb_type": "up"})
    assert up_1.status_code == 200

    # Same vote again should delete the existing thumb (no new one created)
    up_2 = client.post(f"/thumbs/{idea_id}/add_thumb", params={"new_thumb_type": "up"})
    assert up_2.status_code == 200

    fetched = client.get(f"/ideas/{idea_id}")
    assert fetched.status_code == 200
    body = fetched.json()
    assert body["thumbs_up"] == 0
    assert body["thumbs_down"] == 0


def test_thumbs_switch_vote_replaces_thumb(client):
    idea = client.post("/ideas/new", json={"concept": "Switch test"}).json()
    idea_id = idea["id"]

    up = client.post(f"/thumbs/{idea_id}/add_thumb", params={"new_thumb_type": "up"})
    assert up.status_code == 200

    down = client.post(f"/thumbs/{idea_id}/add_thumb", params={"new_thumb_type": "down"})
    assert down.status_code == 200

    fetched = client.get(f"/ideas/{idea_id}")
    assert fetched.status_code == 200
    body = fetched.json()
    assert body["thumbs_up"] == 0
    assert body["thumbs_down"] == 1
