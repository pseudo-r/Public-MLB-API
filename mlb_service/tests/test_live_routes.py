from unittest.mock import MagicMock, patch

import pytest
from rest_framework.test import APIClient


@pytest.mark.parametrize("path,method", [('teams/147/roster/', 'get_team_roster'), ('games/777001/plays/', 'get_game_play_by_play'), ('divisions/', 'get_divisions')])
def test_live_routes(path, method):
    with patch("apps.core.upstream.MLBClient") as factory:
        client = factory.return_value
        client.__enter__.return_value = client
        getattr(client, method).return_value = MagicMock(data={"fixture": True})
        response = APIClient().get("/api/v1/live/" + path)
        assert response.status_code == 200
        assert response.json() == {"fixture": True}
        getattr(client, method).assert_called_once()
