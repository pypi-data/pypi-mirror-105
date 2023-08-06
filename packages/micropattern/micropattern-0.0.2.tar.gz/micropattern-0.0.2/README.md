# micropattern
Common package
```sh
pip install micropattern
```

### Using Rabbit MQ `basic_publish` with helper
```python
from micropattern.utils.mq import BasicPublish
 queue = BasicPublish(
     host=MQ_HOST,
     port=MQ_PORT,
     username=MQ_USERNAME,
     password=MQ_PASSWORD,
     queue_name='test_queue',
     debug=True
 )

 with queue() as publisher:
     publisher.enqueue("{'test': 'test'}")
```

### Using remote config with `Registry` helper
1. Define your configs at: `http://10.15.0.7:8000`  
   E.g. `dummy` configs
   ```json
    {
       "name": "Hai Tran",
       "phone": 1234567890
    }
    ```
2. Map your config to a class inherited `Registry`
   ```python
   from micropattern.registry import Registry
   class DummyConfig(Registry):
        name: str
        phone: int
        def __init__(self):
            super().__init__(key='dummy')
   ```

3. Create an instance of config, and just `dot` attribute, your remote configs will be loaded to the instance
   ```python
   dummy_cfg = DummyConfig()
   print(dummy_cfg.name)
   print(dummy_cfg.phone)
   ```

4. Save remote configs, your configs automatically submitted after leaving the context
   ```python
   with dummy_cfg() as cfg:
       cfg.name = 'New name'
       cfg.phone = 987654321
   ```
