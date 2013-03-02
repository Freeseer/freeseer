# http://apiwiki.justin.tv/mediawiki/index.php/Python_Library_v2

import simplejson
import jtv_client
from urllib import urlencode

###
# Sample usage
###

# User.jtv_client = jtv_client.JtvClient('XXX', 'XXX')
# emmett = User.show('emmett')
# print emmett.profile_url

# access_token = oauth.OAuthToken('XXX', 'XXX')
# me = User.whoami(access_token)
# me.location = 'At a place %s' % random.random()
# print me.update()

# print [friend.login for friend in emmett.friends(limit=30)]
# print [favorite.login for favorite in emmett.favorites()]
# print [event.title for event in emmett.events()]
# print [friend.login for friend in User.friends_of('emmett', offset=100)]

# newuser = User({'login': 'XXXXXXX', 'birthday': 'YYYY-MM-DD', 'password': 'XXXXX', 'email': 'XXX@XXX.XX'})
# print newuser.create()


class AccessTokenRequired(Exception):
    """
    Raised if the method called requires an access token to act on behalf of a user,
    but no access token was provided
    """
    pass

class UnwritableAttribute(Exception):
    """
    Raised if an attribute assignment attempts to overwrite a read-only attribute
    """
    pass

class Model(object):
    """
    The base class for the JTV rest library models. Provides the functionality shared
    between all models.
    """
    jtv_client = None
    model_name = None
    primary_key = None
    writable_attributes = []

    def __init__(self, attributes, access_token=None):
        """
        Creates a new model from a dict of attributes, and optionally an access token to
        use when making requests on from that object.
        """
        self.changed = []
        self.access_token = access_token
        self.attributes = attributes # comes last because this activates our custom .__setattr__

    def __repr__(self):
        return "%s(%s)" % (self.__class__.__name__, repr(self.attributes))

    def __getattr__(self, name):
        """
        Returns a model attribute if the attribute does not exist on the python object
        """
        if name in self.attributes:
            return self.attributes[name]
        else:
            raise AttributeError, name

    def __setattr__(self, name, value):
        """
        Sets as a model attribute if the attribute does not exist as a python object attribute
        """
        if not hasattr(self, 'attributes'):
            object.__setattr__(self, name, value)

        if name in self.__dict__:
            self.__dict__[name] = value
            return

        if name not in self.writable_attributes:
            raise UnwritableAttribute, "%s has no writable attribute %s" % (repr(self.model_name), repr(name))

        if self.attributes[name] != value:
            self.changed.append(name)
            self.attributes[name] = value

    def update(self):
        """
        Saves changes to the model to Justin.tv. If no changes have been made, is a no-op.
        On success: returns dict of model attributes for updated model
        On failure: returns dict of {'error': 'error message', 'url': '/model_name/update.json'}
        """
        if not self.changed:
            return self.attributes

        if not self.access_token:
            raise AccessTokenRequired, "This object does not have an associated access token and thus may not be updated"

        params = dict((attr, self.attributes[attr]) for attr in self.changed)
        self.changed = []
        url = '/%s/update.json' % self.model_name
        response = self.jtv_client.post(url, params, self.access_token).read()
        return simplejson.loads(response)

    def create(self):
        """
        Creates the model on Justin.tv.
        On success:
        For users/channels, returns dict of {'model_name': attributes, 'oauth': {'access_token': 'XXX', 'access_token_secret': 'XXX}}
        For all others, returns a dict of model attributes
        On failure: returns dict of {'error': 'error message', 'url': '/model_name/create.json'}
        """
        url = '/%s/create.json' % self.model_name
        response = self.jtv_client.post(url, self.attributes).read()
        return simplejson.loads(response)

    def get_related(self, request, constructor, **kwargs):
        """
        Return other models related to this one.
        Keyword arguments:
        offset -- offset from the start of the related list to begin returning from
        limit  -- maximum number of related models to return
        """
        if not self.primary_key:
            raise Exception, "%s does not support the show() method" % self.__class__.__name__

        path = '/%s/%s/%s.json' % (self.model_name, request, getattr(self, self.primary_key))
        for k, v in kwargs.items():
            if v == None:
                del kwargs[k]
        if kwargs:
            path += '?' + urlencode(kwargs)
        response = self.jtv_client.get(path).read()
        return [constructor(attrs) for attrs in simplejson.loads(response)]

class User(Model):
    """
    User objects from the Justin.tv API: http://apiwiki.justin.tv/mediawiki/index.php/Returned_Objects#User_Object
    """

    model_name = "user"
    writable_attributes = [
        'broadcaster', 'favorite_quotes', 'location',
        'name', 'profile_about', 'profile_about', 'profile_image',
        'profile_background_color', 'profile_header_bg_color',
        'profile_header_border_color', 'profile_header_text_color',
        'profile_link_color'
    ]
    primary_key = "login"

    @classmethod
    def show(self, login):
        """
        Return the user object matching login.
        If the user doesn't exist, you will get a user object with the following dict:
            User({
                "error": "Couldn't find user",
                "url": "/api/user/show/-login-.json"
            })
        You'll want to check the response:
        may_not_exist = User.show('may_not_exist')
        if may_not_exist.error: return False
        """
        response = self.jtv_client.get('/user/show/%s.json' % login).read()
        return self(simplejson.loads(response))

    @classmethod
    def whoami(self, access_token):
        """
        Returns the user for a given oauth token.
        """
        response = self.jtv_client.get('/account/whoami.json', access_token).read()
        return self(simplejson.loads(response), access_token)

    @classmethod
    def friends_of(self, login, limit=None, offset=None):
        """
        Returns the friends of the user specified by login (a list of User objects)
        """
        return User({'login': login}).friends(limit=limit, offset=offset)

    def friends(self, limit=None, offset=None):
        """
        Returns the friends of this user (a list of User objects)
        """
        return self.get_related('friends', User, limit=limit, offset=offset)

    @classmethod
    def favorites_of(self, login, limit=None, offset=None):
        """
        Returns the favorites of the user specified by login (a list of Channel objects)
        """
        return User({'login': login}).favorites(limit=limit, offset=offset)

    def favorites(self, limit=None, offset=None):
        """
        Returns the favorites of this user (a list of Channel objects)
        """
        return self.get_related('favorites', Channel, limit=limit, offset=offset)

    @classmethod
    def events_of(self, login, limit=None, offset=None):
        """
        Returns the events subscribed to by the user specified by login (a list of Event objects)
        """
        return User({'login': login}).events(limit=limit, offset=offset)

    def events(self, limit=None, offset=None):
        """
        Returns the events subscribed to by this user (a list of Event objects)
        """
        return self.get_related('events', Event, limit=limit, offset=offset)

class Channel(Model):
    """
    Channel objects from the Justin.tv API: http://apiwiki.justin.tv/mediawiki/index.php/Returned_Objects#Channel_Object
    """
    model_name = "channel"
    primary_key = "login"

    @classmethod
    def show(self, login):
        """
        Return the channel object matching login.
        If the user doesn't exist, you will get a channel object with the following dict:
            Channel({
                "error": "Couldn't find channel",
                "url": "/api/user/show/-login-.json"
            })
        You'll want to check the response:
        may_not_exist = Channel.show('may_not_exist')
        if may_not_exist.error: return False
        """
        response = self.jtv_client.get('/channel/show/%s.json' % login).read()
        return self(simplejson.loads(response))


    @classmethod
    def events_of(self, login, limit=None, offset=None):
        """
        Returns the events owned by the channel specified by login (a list of Event objects)
        """
        return User({'login': login}).events(limit=limit, offset=offset)

    def events(self, limit=None, offset=None):
        """
        Returns the events owned by this channel (a list of Event objects)
        """
        return self.get_related('events', Event, limit=limit, offset=offset)


class Event(Model):
    """
    Event objects from the Justin.tv API: http://apiwiki.justin.tv/mediawiki/index.php/Returned_Objects#Event_Object
    """
    model_name = "event"
    primary_key = "id"

class Clip(Model):
    """
    Clip objects from the Justin.tv API: http://apiwiki.justin.tv/mediawiki/index.php/Returned_Objects#Clip_Object
    """
    model_name = "clip"
    primary_key = "id"

class Event(Model):
    """
    Archive objects from the Justin.tv API: http://apiwiki.justin.tv/mediawiki/index.php/Returned_Objects#Archive_Object
    """
    model_name = "archive"
    primary_key = "id"

class Callback(Model):
    """
    Callback objects from the Justin.tv API: http://apiwiki.justin.tv/mediawiki/index.php/Returned_Objects#Callback_Object
    """
    model_name = "callback"
    primary_key = None

class Stream(Model):
    """
    Stream objects from the Justin.tv API: http://apiwiki.justin.tv/mediawiki/index.php/Returned_Objects#Event_Object
    """
    model_name = "stream"
    primary_key = None

