from django.template import Library, Node, TemplateSyntaxError
from django.template import Variable, resolve_variable
from django.utils.translation import ugettext as _
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
#from books.models import Book

register = Library()
from duoshuo import DuoshuoAPI

ds = DuoshuoAPI(client_id='dfsfsdsfdfsd',secret='w32234dff' )

def get_contenttype_kwargs(content_object):
    """
    Gets the basic kwargs necessary for form submission url
    """
    kwargs = {'content_type_id':
        ContentType.objects.get_for_model(content_object).id,
    'object_id':
        getattr(content_object, 'pk',
            getattr(content_object, 'id')),
    }
    return kwargs
 
def get_book_form_url(content_object):
    """
    prints url for form action
    """
    kwargs = get_contenttype_kwargs(content_object)
    return reverse('new_book', kwargs=kwargs)
 
class BooksForObjectsNode(Node):
    """
    Get the books and add to the context
    """
    def __init__(self, obj, context_var):
        self.obj = Variable(obj)
        self.context_var = context_var
 
    def render(self, context):
        content_type = ContentType.objects.get_for_model(
            self.obj.resolve(context))
        # create the template var by adding to context
        context[self.context_var] = \
            Book.objects.filter( # find all books for object
                content_type__pk = content_type.id,
                object_id = self.obj.resolve(context).id
            )
        return ''
 
def books_for_object(parser, token):
    """
    Retrieves a list of books for given object
    {% books_for_object foo_object as book_list %}
    """

    return BooksForObjectsNode(bits[1], bits[3])

 
class BookFormNode(Node):
    """
    Get the form and add it to the context
    """
    def __init__(self, short_name=None):
        self.short_name = short_name
    def render(self, context):
        # create the template var by adding to context
        return '<script>alert('+short_name+')</script>'

COMMENTS = 'register.html'

@register.inclusion_tag('duoshuo_comments.html')
def duoshuo_comments(short_name):
    return {'short_name': short_name}

def get_duoshuo_oauth_url(redirect_uri):
    return ds.get_url(redirect_uri=redirect_uri)

# register these tags for use in template files
register.tag('books_for_object', books_for_object)
register.simple_tag(get_book_form_url)
register.simple_tag(get_duoshuo_oauth_url)
