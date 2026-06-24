import unittest
from unittest.mock import patch, MagicMock
import worldcup

class TestSaveTeam(unittest.TestCase):
  @patch('worldcup.getDB')
  def test_saveTeam_invalid_team(self, mock_getdb):
    mock_conn = MagicMock()
    mock_conn.execute.return_value.fetchone.return_value = None
    mock_getdb.return_value = mock_conn
    
    result = worldcup.saveTeam("Fake team")
    self.assertFalse(result)

  @patch('worldcup.getDB')
  def test_saveTeam_valid_team(self, mock_getdb):
    mock_conn = MagicMock()
    mock_conn.execute.return_value.fetchone.return_value = (42,)
    mock_getdb.return_value = mock_conn

    result = worldcup.saveTeam("Fake team")
    self.assertTrue(result)

class TestFindSpotlightMatch(unittest.TestCase):
  @patch('worldcup.getMatchHype')
  def test_findSpotlightMatch_one_favorite(self, mock_getMatchHype):
    matches = [
        {
            "home_team_id": 1,
            "away_team_id": 2,
            "home_team_name": "Mexico",
            "away_team_name": "Spain",
            "utc_date": "2026-06-24T18:00:00Z"
        }
    ]
    favorites = [1]
    mock_getMatchHype.return_value = True

    result = worldcup.findSpotlightMatch(matches, favorites)
    self.assertTrue(result)
  
  @patch('worldcup.getMatchesHype')
  def test_findSpotlightMatch_no_favorite(self, mock_getMatchesHype):
    matches = [
        {
            "home_team_id": 1,
            "away_team_id": 2,
            "home_team_name": "Mexico",
            "away_team_name": "Spain",
            "utc_date": "2026-06-24T18:00:00Z"
        },
        {
           "home_team_id": 4,
            "away_team_id": 3,
            "home_team_name": "USA",
            "away_team_name": "Germany",
            "utc_date": "2026-06-24T18:00:00Z"
        }
    ]
    favorites = [5, 6]
    mock_getMatchesHype.return_value = True

    result = worldcup.findSpotlightMatch(matches, favorites)
    self.assertTrue(result)

  @patch('worldcup.getMatchHype')
  def test_findSpotlightMatch_multiple_favorite(self, mock_getMatchHype):
    matches = [
        {
            "home_team_id": 1,
            "away_team_id": 2,
            "home_team_name": "Mexico",
            "away_team_name": "Spain",
            "utc_date": "2026-06-24T18:00:00Z"
        },
        {
           "home_team_id": 4,
            "away_team_id": 3,
            "home_team_name": "USA",
            "away_team_name": "Germany",
            "utc_date": "2026-06-24T18:00:00Z"
        }
    ]
    favorites = [2, 4]
    mock_getMatchHype.return_value = True
    with patch('builtins.input', return_value = '1'):
      result = worldcup.findSpotlightMatch(matches, favorites)
      self.assertTrue(result)