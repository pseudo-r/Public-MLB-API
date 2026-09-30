import httpx
import pytest

from clients.mlb_client import MLBClient


@pytest.mark.parametrize("method,args,url", [
    ("get_team_roster", (147, 2026), "v1/teams/147/roster?season=2026"),
    ("get_divisions", (), "v1/divisions?sportId=1"),
    ("get_game_play_by_play", (777001,), "v1/game/777001/playByPlay"),
    ("get_game_feed", (777001,), "v1.1/game/777001/feed/live"),
])
def test_new_routes(httpx_mock, method, args, url):
    httpx_mock.add_response(url="https://statsapi.mlb.com/api/" + url, json={"ok": True})
    with MLBClient() as client:
        assert getattr(client, method)(*args).data == {"ok": True}

@pytest.mark.parametrize("status", [400, 403, 404, 429])
def test_terminal_errors_are_not_retried(httpx_mock, status):
    httpx_mock.add_response(status_code=status)
    with MLBClient(max_retries=3) as client, pytest.raises(httpx.HTTPStatusError):
        client.get_teams()
    assert len(httpx_mock.get_requests()) == 1
