# Duoshuo Python SDK

ds = DuoshuoAPI(client_id=client_id, secret=secret)

ds.get_url(redirect_uri=redirect_uri)

ds.get_token(redirect_uri=redirect_uri, code=code)

ds.api('get.user', {id:1})
