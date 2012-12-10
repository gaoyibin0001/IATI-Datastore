from iatilib import frontend
import unittest
import json

class IatiFrontendTestCase(unittest.TestCase):
    def setUp(self):
        frontend.app.config['TESTING'] = True
        self.app = frontend.app.test_client()

    def tearDown(self):
        pass

    def _get_json(self,url):
        rv = self.app.get(url)
        data = json.loads(rv.data)
        assert data['ok'] is True 
        return data, rv

    def test_health(self):
        data,rv = self._get_json('/api/1/health.json')
        assert 'DB contains' in data['raw_xml'], json.dumps(data,indent=2)

    # These argument tests come from the IATI API Guidelines:
    # https://docs.google.com/document/d/1gxvmYZSDXBTSMAU16bxfFd-hn1lYVY1c2olkXbuPBj4/edit 
    def test_args_1(self):
        data,rv = self._get_json('/api/1/debug/args.json?sector=60061')
        assert data['raw_xml']['processed'][0]=='//sector[@vocabulary=\'DAC\']/@code=60061', json.dumps(data,indent=2)
    def test_args_2(self):
        data,rv = self._get_json('/api/1/debug/args.json?sector.text=Debt')
        assert data['raw_xml']['processed'][0]=='//sector[@vocabulary=\'DAC\']/text()=Debt', json.dumps(data,indent=2)
    def test_args_3(self):
        data,rv = self._get_json('/api/1/debug/args.json?participating-org=GB-1-123')
        assert data['raw_xml']['processed'][0]=='//participating-org/@ref=GB-1-123', json.dumps(data,indent=2)
    def test_args_4(self):
        data,rv = self._get_json('/api/1/debug/args.json?participating-org.text=\'Oxfam\'')
        assert data['raw_xml']['processed'][0]=='//participating-org/text()=\'Oxfam\'', json.dumps(data,indent=2)
    def test_args_5(self):
        data,rv = self._get_json('/api/1/debug/args.json?iati-identifier=GB-1-123')
        assert data['raw_xml']['processed'][0]=='//iati-identifier/text()=GB-1-123', json.dumps(data,indent=2)
    def test_args_6(self):
        data,rv = self._get_json('/api/1/debug/args.json?location_name=Oxford')
        assert data['raw_xml']['processed'][0]=='//location/name/text()=Oxford', json.dumps(data,indent=2)
    def test_args_7(self):
        data,rv = self._get_json('/api/1/debug/args.json?transaction_value=1000')
        assert data['raw_xml']['processed'][0]=='//transaction/value/text()=1000', json.dumps(data,indent=2)
