import pydash

from hestia_earth.orchestrator.log import logger
from hestia_earth.orchestrator.utils import update_node_version, _average


def _should_merge(source: dict, dest: dict, key: str, threshold: float):
    source_value = _average(source.get(key), None)
    dest_value = _average(dest.get(key), None)
    diff = None if source_value is None or dest_value is None else abs(source_value - dest_value)
    logger.debug('merge %s with threshold=%s, current diff=%s', key, threshold, diff)
    return diff is None or \
        (source_value == 0 and diff > threshold) or \
        (source_value != 0 and diff / source_value > threshold)


def merge(source: dict, dest: dict, version: str, args={}):
    [key, threshold] = args.get('replaceThreshold', [None, 0])
    should_merge = True if key is None else _should_merge(source, dest, key, threshold)
    return update_node_version(version, pydash.objects.merge({}, source, dest), source) if should_merge else source
