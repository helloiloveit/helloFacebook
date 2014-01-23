# -*- coding: utf-8 -*- 

#########################################################################
## This is a samples controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - call exposes all registered services (none by default)
#########################################################################  
import pdb;

def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html
    """

    user = auth.user
    print user
    comment_list = db(db.comment_tbl).select()
    print' comment_list = ', comment_list
    question_tbl = db(db.question_tbl).select()
    print' question_tbl = ', question_tbl
    if user:
        response.flash = T('You are %(name)s', dict(name=user['first_name']))
        return dict(message=T('Hello, Facebook is telling that you are %(first_name)s %(last_name)s', dict(first_name=user['first_name'], last_name=user['last_name'])))
    response.flash = T('Welcome to web2py')
    return dict(message=T('Hello, please login aa   '))

def user():
    """
    exposes:
    http://..../[app]/default/user/login 
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    import pdb;pdb.set_trace()
    return dict(form=auth())


def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request,db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    session.forget()
    return service()


