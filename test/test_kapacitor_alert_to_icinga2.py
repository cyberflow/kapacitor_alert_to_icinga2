#!/usr/bin/env python
import pytest
import os
import inspect
import sys

currentdir = os.path.dirname(
    os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)


@pytest.fixture(scope="module")
def plugin(request):
    import kapacitor_alert_to_icinga2
    return kapacitor_alert_to_icinga2


@pytest.mark.parametrize('input, output', [
    ['OK', 0],
    ['INFO', 0],
    ['WARNING', 1],
    ['CRITICAL', 2],
    ['SOMETHING', 3]
])
def test_parse_result(plugin, input, output):
    assert plugin.parse_result(input) == output

kapacitor_data_sample = {
  'id':'conntrack_value',
  'message':'application.servers.com is OK conntrack value: 50',
  'details':'{}',
  'time':'2017-06-27T08:21:36.062529791Z',
  'duration':19999978774,
  'level':'OK',
  'data':{'series':
    [{'name':'conntrack_value',
      'tags':{'host':'application.servers.com',
              'type':'percent',
              'type_instance':'used'},
      'columns':['time','value'],
      'values':[['2017-06-27T08:21:36.062529791Z',50]]
    }]
  }}


def test_extract_host(plugin):
    assert plugin.extract_host(kapacitor_data_sample) == 'application.servers.com'


def test_extract_service(plugin):
    assert plugin.extract_service(kapacitor_data_sample) == 'conntrack_value'


def test_gen_payload(plugin):
    assert plugin.gen_payload(kapacitor_data_sample) == '{"plugin_output": "application.servers.com is OK conntrack value: 50", "exit_status": 0}'


def test_modify_host(plugin):
    assert plugin.modify_host('application.servers.com', '.servers.com') == 'application'


if __name__ == "__main__":
    ourfilename = os.path.abspath(inspect.getfile(inspect.currentframe()))
    currentdir = os.path.dirname(ourfilename)
    parentdir = os.path.dirname(currentdir)
    file_to_test = os.path.join(
        parentdir,
        # os.path.basename('.'),
        os.path.basename(ourfilename).replace('test_', '', 1)
    )
    pytest.main([
     "-vv",
     "--cov", file_to_test,
     "--cov-report", "term-missing"
     ] + sys.argv)
