import unittest
import simplegeo

class ClientTest(unittest.TestCase):
    MY_OAUTH_KEY = 'my_key'
    MY_OAUTH_SECRET = 'my_secret'
    TESTING_LAYER = 'my_test_layer'
    
    def setUp(self):
        self.client = simplegeo.Client(self.MY_OAUTH_KEY, self.MY_OAUTH_SECRET)
        #self.api_error = simplegeo.APIError(code='100', message='Mock Message', headers=['Mock Header'])
        
    #def tearDown(self):
    #    records = self.client.get_records(self.TESTING_LAYER, ['1', '2', '3', '4'])
    #    print records
    #    for record in records:
    #        self.client.delete_record(self.TESTING_LAYER, record['id'])
        
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
        new_record = simplegeo.Record(layer=self.TESTING_LAYER, id='1', lat='36.025776999999998', lon='-86.656917000000007', type='person', name='Testy McGillicuddy 1')
        self.client.add_record(new_record)
        record = self.client.get_record(self.TESTING_LAYER, '1')
        self.assertTrue(record)
        
    def test_add_records_exception(self):
        records = [simplegeo.Record(layer=self.TESTING_LAYER, id='2', lat='36.025776999999998', lon='-86.656917000000007', type='person', name='Testy McGillicuddy 2'),
                simplegeo.Record(layer=self.TESTING_LAYER, id='3', lat='36.025776999999998', lon='-86.656917000000007', type='person', name='Testy McGillicuddy 3'),
                simplegeo.Record(layer=self.TESTING_LAYER, id='4', lat='36.025776999999998', lon='-86.656917000000007', type='person', name='Testy McGillicuddy 4')]
        self.assertRaises(Exception, self.client.add_records, records)
    
    def test_add_records_success(self):
        records = [simplegeo.Record(layer=self.TESTING_LAYER, id='2', lat='36.025776999999998', lon='-86.656917000000007', type='person', name='Testy McGillicuddy 2'),
                simplegeo.Record(layer=self.TESTING_LAYER, id='3', lat='36.025776999999998', lon='-86.656917000000007', type='person', name='Testy McGillicuddy 3'),
                simplegeo.Record(layer=self.TESTING_LAYER, id='4', lat='36.025776999999998', lon='-86.656917000000007', type='person', name='Testy McGillicuddy 4')]
        self.client.add_records(self.TESTING_LAYER, records)
        records = self.client.get_records(self.TESTING_LAYER, ['2','3','4'])
        self.assertTrue(records)
        
    def test_get_record_exception(self):
        self.assertRaises(Exception, self.client.get_record, 'crispy.bacon')
        
    def test_get_record_success(self):
        new_record = simplegeo.Record(layer=self.TESTING_LAYER, id='1', lat='36.025776999999998', lon='-86.656917000000007', type='person', name='Testy McGillicuddy 1')
        self.client.add_record(new_record)
        record = self.client.get_record(self.TESTING_LAYER, '1')
        self.assertTrue(record)
        
    def test_get_records_exception(self):
        self.assertRaises(Exception, self.client.get_records, ['crispy.bacon', 'runny.eggs', 'warm.juice'])
    
    def test_get_records_success(self):
        records = [simplegeo.Record(layer=self.TESTING_LAYER, id='2', lat='36.025776999999998', lon='-86.656917000000007', type='person', name='Testy McGillicuddy 2'),
                simplegeo.Record(layer=self.TESTING_LAYER, id='3', lat='36.025776999999998', lon='-86.656917000000007', type='person', name='Testy McGillicuddy 3'),
                simplegeo.Record(layer=self.TESTING_LAYER, id='4', lat='36.025776999999998', lon='-86.656917000000007', type='person', name='Testy McGillicuddy 4')]
        self.client.add_records(self.TESTING_LAYER, records)
        records = self.client.get_records(self.TESTING_LAYER, ['1','2','3','4'])
        self.assertTrue(records)
    
    def test_get_history_exception(self):
        self.assertRaises(Exception, self.client.get_history, '1')
        
    def test_get_history_success(self):
        history = self.client.get_history(self.TESTING_LAYER, '1')
        self.assertTrue(history)
        
    def test_delete_record_exception(self):
        new_record = simplegeo.Record(layer=self.TESTING_LAYER, id='1', lat='36.025776999999998', lon='-86.656917000000007', type='person', name='Testy McGillicuddy 1')
        self.client.add_record(new_record)
        
        self.assertRaises(Exception, self.client.delete_record, None, '1')
        self.assertRaises(Exception, self.client.delete_record, self.TESTING_LAYER, 'crispy.bacon')
        
    def test_delete_record_success(self):
        records = [simplegeo.Record(layer=self.TESTING_LAYER, id='1d', lat='36.025776999999998', lon='-86.656917000000007', type='person', name='Testy McGillicuddy 2'),
                simplegeo.Record(layer=self.TESTING_LAYER, id='2d', lat='36.025776999999998', lon='-86.656917000000007', type='person', name='Testy McGillicuddy 3'),
                simplegeo.Record(layer=self.TESTING_LAYER, id='3d', lat='36.025776999999998', lon='-86.656917000000007', type='person', name='Testy McGillicuddy 4')]
        self.client.add_records(self.TESTING_LAYER, records)
        
        self.failIf(self.client.delete_record(self.TESTING_LAYER, '1d'))
        self.failIf(self.client.delete_record(self.TESTING_LAYER, '2d'))
        self.failIf(self.client.delete_record(self.TESTING_LAYER, '3d'))
        
        self.assertRaises(Exception, self.client.get_record, self.TESTING_LAYER, '1d')
        self.assertRaises(Exception, self.client.get_record, self.TESTING_LAYER, '2d')
        self.assertRaises(Exception, self.client.get_record, self.TESTING_LAYER, '3d')

if __name__ == '__main__':
    unittest.main()
