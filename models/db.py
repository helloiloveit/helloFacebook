# -*- coding: utf-8 -*- 

#########################################################################
## This scaffolding model makes your app work on Google App Engine too
#########################################################################


if request.env.web2py_runtime_gae:            # if running on Google App Engine
    db = DAL('gae')                           # connect to Google BigTable
    session.connect(request, response, db = db) # and store sessions and tickets there
    ### or use the following lines to store sessions in Memcache
    # from gluon.contrib.memdb import MEMDB
    # from google.appengine.api.memcache import Client
    # session.connect(request, response, db = MEMDB(Client()))
else:                                         # else use a normal relational database
    db = DAL('sqlite://storage.sqlite')       # if not, use SQLite or other DB
## if no need for session
# session.forget()

#########################################################################
## Here is sample code if you need for 
## - email capabilities
## - authentication (registration, login, logout, ... )
## - authorization (role based authorization)
## - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
## - crud actions
## (more options discussed in gluon/tools.py)
#########################################################################

from gluon.tools import *
mail = Mail()                                  # mailer
auth = Auth(globals(),db)                      # authentication/authorization
crud = Crud(globals(),db)                      # for CRUD helpers using auth
service = Service(globals())                   # for json, xml, jsonrpc, xmlrpc, amfrpc

mail.settings.server = 'logging' or 'smtp.gmail.com:587'  # your SMTP server
mail.settings.sender = 'you@gmail.com'         # your email
mail.settings.login = 'username:password'      # your credentials or None

auth.settings.hmac_key = 'sha512:12660f29-c206-409f-8215-ed11cc55ccf2'   # before define_tables()
# define the auth_table before call to auth.define_tables()
auth_table = db.define_table(
    auth.settings.table_user_name,
    Field('first_name', length=128, default=""),
    Field('last_name', length=128, default=""),
    #Field('username', length=128, default="", unique=True),
    Field('email', length=128, default='', unique=True),
    Field('username', length=128, default=""),
    Field('password', 'password', length=256,
          readable=False, label='Password'),
    Field('registration_key', length=128, default= "",
          writable=False, readable=False))

auth_table.username.requires = IS_NOT_IN_DB(db, auth_table.username)

auth.define_tables()                           # creates all needed tables
auth.settings.mailer = mail                    # for user email verification
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.messages.verify_email = 'Click on the link http://'+request.env.http_host+URL(r=request,c='default',f='user',args=['verify_email'])+'/%(key)s to verify your email'
auth.settings.reset_password_requires_verification = True
auth.messages.reset_password = 'Click on the link http://'+request.env.http_host+URL(r=request,c='default',f='user',args=['reset_password'])+'/%(key)s to reset your password'

crud.settings.auth = None                      # =auth to enforce authorization on crud

################################################################################
## use fb auth
## for facebook "graphbook" application
################################################################################
db.define_table('article_tag',
    Field('name', 'string')
    )


db.define_table('question_tbl',
    Field('article_header', 'text'),
    Field('article_introduction', 'text'),
    Field('story', 'text'),
    Field('writer', 'reference auth_user'))

db.define_table('tag_tbl',
    Field('question_info',db.question_tbl),
    Field('tag_info', db.article_tag))


db.define_table('follow_tbl',
    Field('blog_info',db.question_tbl),
    Field('user_info', 'reference auth_user'))

db.define_table('comment_tbl',
    Field('comment_info', 'text'),
    Field('question_info',db.question_tbl),
    Field('author_info', 'reference auth_user'))



db.define_table('pic_store',
    Field('pic','upload')
    )



import sys, os
path = os.path.join(request.folder, 'modules')
if not path in sys.path:
    sys.path.append(path)

from facebook import GraphAPI, GraphAPIError
from gluon.contrib.login_methods.oauth20_account import OAuthAccount
class FaceBookAccount(OAuthAccount):
    """OAuth impl for FaceBook"""
    AUTH_URL="https://graph.facebook.com/oauth/authorize"
    TOKEN_URL="https://graph.facebook.com/oauth/access_token"

    def __init__(self, g):

        #import pdb;pdb.set_trace()
        OAuthAccount.__init__(self, g, "248577781948157", "a5abf06a362c8f0fa4cf5da339906185",
                              self.AUTH_URL, self.TOKEN_URL,
                              scope='user_photos,friends_photos')
        self.graph = None


    def get_user(self):
        '''Returns the user using the Graph API.
        '''
        #import pdb;pdb.set_trace()
        if not self.accessToken():
            print' return none'
            return None

        if not self.graph:
            self.graph = GraphAPI((self.accessToken()))

        user = None
        try:
            user = self.graph.get_object("me")
        except GraphAPIError, e:
            self.session.token = None
            self.graph = None


        if user:
            import pdb;pdb.set_trace()
            print user
            first_name = user['first_name']
            import pdb;pdb.set_trace()
            last_name = user['last_name']
            import pdb;pdb.set_trace()
            username = user['id']
            import pdb;pdb.set_trace()
            email = user['email']

            return dict(first_name = user['first_name'],
                        last_name = user['last_name'],
                        email    = user['email'],
                        username = user['id'])


crud.settings.auth = None                      # =auth to enforce authorization on crud
auth.settings.actions_disabled=['register','change_password','request_reset_password','profile']
auth.settings.login_form=FaceBookAccount(globals())
#auth.settings.login_next=URL(f='index')
#########################################################################
## Define your tables below (or better in another model file) for example
##
## >>> db.define_table('mytable',Field('myfield','string'))
##
## Fields can be 'string','text','password','integer','double','boolean'
##       'date','time','datetime','blob','upload', 'reference TABLENAME'
## There is an implicit 'id integer autoincrement' field
## Consult manual for more options, validators, etc.
##
## More API examples for controllers:
##
## >>> db.mytable.insert(myfield='value')
## >>> rows=db(db.mytable.myfield=='value').select(db.mytable.ALL)
## >>> for row in rows: print row.id, row.myfield
#########################################################################
