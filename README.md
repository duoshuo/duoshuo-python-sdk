# Duoshuo Python SDK

本SDK支持用Python语言开发的网站，对其提供[多说]插件的支持，您可以只调用提供的函数，也可以作为一个Django应用来使用。


# Requirements

Python 2.6+

simplejson (option)

# Usage


    ds = DuoshuoAPI(client_id=client_id, secret=secret)

    ds.get_url(redirect_uri=redirect_uri)

    ds.get_token(redirect_uri=redirect_uri, code=code)

    ds.api('get.user', {id:1})