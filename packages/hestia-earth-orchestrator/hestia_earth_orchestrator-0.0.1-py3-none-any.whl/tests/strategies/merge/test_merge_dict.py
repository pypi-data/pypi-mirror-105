import unittest
from unittest.mock import patch

from hestia_earth.orchestrator.strategies.merge.merge_dict import merge, _should_merge

class_path = 'hestia_earth.orchestrator.strategies.merge.merge_dict'


class TestStrategiesMergeDict(unittest.TestCase):
    def test_should_merge(self):
        key = 'key'
        threshold = 0.1  # 10%
        source = {}
        dest = {}

        # key not in source => merge
        self.assertEqual(_should_merge(source, dest, key, threshold), True)

        # key not in dest => merge
        source[key] = [100]
        self.assertEqual(_should_merge(source, dest, key, threshold), True)

        dest[key] = [90]
        self.assertEqual(_should_merge(source, dest, key, threshold), False)

        dest[key] = [89]
        self.assertEqual(_should_merge(source, dest, key, threshold), True)

        # edge cases
        source[key] = [0]
        dest[key] = [1]
        self.assertEqual(_should_merge(source, dest, key, threshold), True)

        source[key] = [0]
        dest[key] = [0]
        self.assertEqual(_should_merge(source, dest, key, threshold), False)

        source[key] = [1]
        dest[key] = [0]
        self.assertEqual(_should_merge(source, dest, key, threshold), True)

    @patch(f"{class_path}._should_merge", return_value=False)
    def test_merge_no_merge(self, _m1):
        source = {'value': [100]}
        dest = {'value': [50]}
        args = {'replaceThreshold': ['value', 50]}
        # simply return the source
        self.assertEqual(merge(source, dest, '0', args), source)

    @patch(f"{class_path}._should_merge", return_value=True)
    @patch(f"{class_path}.update_node_version", return_value={})
    def test_merge_no_threshold(self, mock_update, _m1):
        source = {'value': [100]}
        dest = {'value': [50]}
        args = {}
        merge(source, dest, '0', args)
        mock_update.assert_called_once()

    @patch(f"{class_path}._should_merge", return_value=True)
    @patch(f"{class_path}.update_node_version", return_value={})
    def test_merge_with_threshold(self, mock_update, _m1):
        source = {'value': [100]}
        dest = {'value': [50]}
        args = {'replaceThreshold': ['value', 50]}
        merge(source, dest, '0', args)
        mock_update.assert_called_once()
