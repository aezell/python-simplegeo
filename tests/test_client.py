import unittest
import simplegeo

class TestClient(unittest.TestCase):
    MY_OAUTH_KEY = 'my_key'
    MY_OAUTH_SECRET = 'my_secret'
    TESTING_LAYER = 'my_test_layer'
    
    # a little nose flavor here to only run this once per class test
    @classmethod
    def setup_class(cls):
        cls.client = simplegeo.Client(cls.MY_OAUTH_KEY, cls.MY_OAUTH_SECRET)
    
    @classmethod
    def teardown_class(cls):
        for id in range(17):
            try:
                cls.client.delete_record(cls.TESTING_LAYER, id)
            except Exception:
                continue
        
    def test_endpoint_exception(self):
        not_an_endpoint = 'bacon.not.crispy'
        self.assertRaises(Exception, self.client.endpoint, not_an_endpoint) 
        
    def test_endpoint_arg_exception(self):
        self.assertRaises(TypeError, self.client.endpoint)
        
    def test_endpoint_success(self):
        testing_layer_endpoint = self.client.endpoint('layer', layer=self.TESTING_LAYER)
        layer_endpoint = '%s/%s/layer/%s.json' % (self.client.uri, self.client.api_version, self.TESTING_LAYER)
        self.assertEqual(testing_layer_endpoint, layer_endpoint)
        
    def test_add_record_exception(self):
        record = simplegeo.Record(layer=self.TESTING_LAYER, id='1', lat='36.025776999999998', lon='-86.656917000000007', type='person', name='Testy McGillicuddy 1')
        delattr(record, 'layer')
        self.assertRaises(Exception, self.client.add_record, record)
        
    def test_add_record_success(self):
        new_record = simplegeo.Record(layer=self.TESTING_LAYER, id='2', lat='36.025776999999998', lon='-86.656917000000007', type='person', name='Testy McGillicuddy 1')
        self.client.add_record(new_record)
        get_record = self.client.get_record(self.TESTING_LAYER, '2')
        record = simplegeo.Record.from_dict(get_record)
        self.assertEqual(new_record, record)
        
    def test_add_records_exception(self):
        records = [simplegeo.Record(layer=self.TESTING_LAYER, id='3', lat='36.025776999999998', lon='-86.656917000000007', type='person', name='Testy McGillicuddy 2'),
                simplegeo.Record(layer=self.TESTING_LAYER, id='4', lat='36.025776999999998', lon='-86.656917000000007', type='person', name='Testy McGillicuddy 3'),
                simplegeo.Record(layer=self.TESTING_LAYER, id='5', lat='36.025776999999998', lon='-86.656917000000007', type='person', name='Testy McGillicuddy 4')]
        self.assertRaises(TypeError, self.client.add_records, records)
    
    def test_add_records_success(self):
        records = [simplegeo.Record(layer=self.TESTING_LAYER, id='5', lat='36.025776999999998', lon='-86.656917000000007', type='person', name='Testy McGillicuddy 2'),
                simplegeo.Record(layer=self.TESTING_LAYER, id='6', lat='36.025776999999998', lon='-86.656917000000007', type='person', name='Testy McGillicuddy 3'),
                simplegeo.Record(layer=self.TESTING_LAYER, id='7', lat='36.025776999999998', lon='-86.656917000000007', type='person', name='Testy McGillicuddy 4')]
        self.client.add_records(self.TESTING_LAYER, records)
        get_records_list = self.client.get_records(self.TESTING_LAYER, ['5','6','7'])
        get_records = [simplegeo.Record.from_dict(get_record) for get_record in get_records_list]
        self.assertEqual(set(get_records), set(records))
        
    def test_get_record_exception(self):
        self.assertRaises(TypeError, self.client.get_record, 'crispy.bacon')
        
    def test_get_record_success(self):
        new_record = simplegeo.Record(layer=self.TESTING_LAYER, id='8', lat='36.025776999999998', lon='-86.656917000000007', type='person', name='Testy McGillicuddy 1')
        self.client.add_record(new_record)
        get_record = self.client.get_record(self.TESTING_LAYER, '8')
        record = simplegeo.Record.from_dict(get_record)
        self.assertEqual(new_record, record)
        
    def test_get_records_exception(self):
        self.assertRaises(TypeError, self.client.get_records, ['crispy.bacon', 'runny.eggs', 'warm.juice'])
    
    def test_get_records_success(self):
        records = [simplegeo.Record(layer=self.TESTING_LAYER, id='9', lat='36.025776999999998', lon='-86.656917000000007', type='person', name='Testy McGillicuddy 2'),
                simplegeo.Record(layer=self.TESTING_LAYER, id='10', lat='36.025776999999998', lon='-86.656917000000007', type='person', name='Testy McGillicuddy 3'),
                simplegeo.Record(layer=self.TESTING_LAYER, id='11', lat='36.025776999999998', lon='-86.656917000000007', type='person', name='Testy McGillicuddy 4')]
        self.client.add_records(self.TESTING_LAYER, records)
        get_records_list = self.client.get_records(self.TESTING_LAYER, ['9','10','11'])
        get_records = [simplegeo.Record.from_dict(get_record) for get_record in get_records_list]
        self.assertEqual(set(get_records), set(records))
    
    def test_get_history_exception(self):
        self.assertRaises(TypeError, self.client.get_history, '2')
        
    def test_get_history_success(self):
        history = self.client.get_history(self.TESTING_LAYER, '2')
        self.assertTrue(history)
        
    def test_delete_record_exception(self):
        new_record = simplegeo.Record(layer=self.TESTING_LAYER, id='14', lat='36.025776999999998', lon='-86.656917000000007', type='person', name='Testy McGillicuddy 1')
        self.client.add_record(new_record)
        self.assertRaises(simplegeo.APIError, self.client.delete_record, None, '14')
        self.assertRaises(simplegeo.APIError, self.client.delete_record, self.TESTING_LAYER, 'crispy.bacon')
        
    def test_delete_record_success(self):
        records = [simplegeo.Record(layer=self.TESTING_LAYER, id='15', lat='36.025776999999998', lon='-86.656917000000007', type='person', name='Testy McGillicuddy 2'),
                simplegeo.Record(layer=self.TESTING_LAYER, id='16', lat='36.025776999999998', lon='-86.656917000000007', type='person', name='Testy McGillicuddy 3'),
                simplegeo.Record(layer=self.TESTING_LAYER, id='17', lat='36.025776999999998', lon='-86.656917000000007', type='person', name='Testy McGillicuddy 4')]
        self.client.add_records(self.TESTING_LAYER, records)
        
        self.failIf(self.client.delete_record(self.TESTING_LAYER, '15'))
        self.failIf(self.client.delete_record(self.TESTING_LAYER, '16'))
        self.failIf(self.client.delete_record(self.TESTING_LAYER, '17'))
        
        self.assertRaises(simplegeo.APIError, self.client.get_record, self.TESTING_LAYER, '15')
        self.assertRaises(simplegeo.APIError, self.client.get_record, self.TESTING_LAYER, '16')
        self.assertRaises(simplegeo.APIError, self.client.get_record, self.TESTING_LAYER, '17')

if __name__ == '__main__':
    unittest.main()
