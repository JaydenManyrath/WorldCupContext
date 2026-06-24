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