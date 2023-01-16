http instance
=============

Your need to provide a http ``instance``, simpler you can just use ``requests.session()`` as your ``instance``

Custom instance example:

.. code-block:: 

    from ac_core.interfaces.HttpUtil import HttpUtilInterface,HttpRespInterface
    class Helper(HttpUtilInterface,HttpRespInterface):
    
        def __init__(self, session):
            self.session = session # not necessary
            self.text = '' # necessary
            self.status_code = 0 # necessary
    
        # necessary
        def get(self, url: str, allow_redirects=True) -> HttpRespInterface:
            resp = self.session.get(url=url, allow_redirects=allow_redirects)
            self.status_code = resp.status_code
            self.text = resp.text
            return self
    
        # necessary
        def post(self, url: str, data: str) -> HttpRespInterface:
            resp = self.session.post(url=url, data=data)
            self.status_code = resp.status_code
            self.text = resp.text
            return self
