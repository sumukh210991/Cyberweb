import logging

from pylons import config, request, response, session, app_globals, tmpl_context as c
from pylons.controllers.util import abort, redirect
from pylons.decorators import jsonify

import sqlalchemy as sa
import sqlalchemy.exceptions as sa_error

# add authentication to control who can access this class.
from authkit.authorize.pylons_adaptors import authorize
from cyberweb.lib import auth

from cyberweb.lib.base import BaseController, render
from cyberweb import model
from cyberweb.model import meta

from datetime import datetime

import cyberweb.lib.helpers as h
from sqlalchemy.orm.attributes import manager_of_class as manager

log = logging.getLogger(__name__)

myclass, myfunc = config.get('authkit.form.authenticate.user.encrypt',':').split(':')
mysecret = config.get('authkit.form.authenticate.user.encrypt.secret','')

try:
    exec('from %s import %s as encrypt' % (myclass,myfunc))
except:
    log.error('No encrypt function is being used for passwords!(%s.%s)',myclass,myfunc)
    encrypt = lambda x,y: x

class AdminController(BaseController):

    # this uses global variable defined lib/helpers.py
    @authorize(auth.is_admin)
    def __before__(self):
        pass

    def __init__(self):
        self.verified = False

    def admin_timeout(self,signum,frame):
        self.verified = False

    def index(self):
         tablename = request.params.get('table')
         if not tablename:
                return self._admin_tasks()
         elif not meta.tables.has_key(tablename):
                return "Table %s does not exist! Add error page later" % tablename

         return self.table(tablename)

    def _admin_tasks(self):
        # Get pending accounts
        c.approve_users = meta.Session.query(model.User).filter(sa.and_(model.User.verified == 0, model.Group.id == 5))
        return render('admin/pending.mako')


    @jsonify
    def verify_user(self):
        id_string = request.params.get('id',None)
        action_string = request.params.get('action',None)
        try:
            id = int(id_string)
            action = int(action_string)
        except:
            return {'Error': True, 'Message': 'Input error. Stop messing with me and contact your administrator.'}

        # Query to make sure the user exists
        if action:
            result = meta.Session.query(model.User).filter(model.User.id == id)
        else:
            result = meta.Session.query(model.CW_UserGroupList).filter(sa.and_(model.CW_UserGroupList.user_id == id,model.CW_UserGroupList.cw_group_id == 5))

        if not result:
            return {'Error': True, 'Message': 'User not found. Stop messing with me and contact your administrator.'}

        # Commit changes to DB
        try:
            if action:
                user = result.one()
                user.verified = True
                meta.Session.add(user)
            else:
                # We expect only 1, but 1+ just means there are repeats.
                for i in result:
                    meta.Session.delete(i)
            meta.Session.commit()
        except:
            meta.Session.rollback()
        else:
            meta.Session.close()
            if action:
                return {'Error':False, 'Message': 'Accepted.'}
            else:
                return {'Error':False, 'Message': 'Rejected.'}

        return {'Error': False, 'Message': 'Success.'}


    def table(self,tablename):
        mytable = self._get_table(tablename)
        if not mytable:
            log.error('Requesting a non-existent table (%s)' % tablename)
            return "Table %s does not exist! Add error page later" % tablename
        log.debug('Displaying table %s' % tablename)

        c.current_subnavtab = tablename

        # Execute select for table data
        select = model.select([mytable])
        c.table = meta.Session.execute(select)

        # Get column names
        c.headers = mytable.columns.keys()

        # Get primary keys and foreign keys
        # We create amapping of foreign keys to the primary keys
        # so that we know their position.
        c.pk_pos = dict()
        c.fkeys = dict()
        header_id = dict()
        pk = mytable.primary_key.columns.keys()
        for i in range(len(c.headers)):
             header_id[c.headers[i]] = i
        for name in pk:
             c.pk_pos[header_id[name]] = header_id[name]

        # Get foreign keys
        c.fkeys = dict()
        for fkey in mytable.foreign_keys:
            local = fkey.parent.name
            target = fkey.target_fullname.split('.')[0]
            ftable = eval('model.t_%s' % target)
            # Execute select for each of the foreign key columns
            fdata = model.select([ftable])
            fkey_data = meta.Session.execute(fdata)
            c.fkeys[header_id[local]] = dict()
            for i in fkey_data.fetchall():
                c.fkeys[header_id[local]][i[0]] = i[1]


        meta.Session.close()
        return render('admin/genadmin.mako')

    @jsonify
    def get_row_json(self,tablename,id):
        id = int(id)
        mytable = self._get_table(tablename)
        h = mytable.columns.keys()
        pk = mytable.c.get(mytable.primary_key.columns.keys()[0])

        if id != 0:
            select = model.select([mytable], (pk == id))
            row = meta.Session.execute(select).fetchone()

        # Populate an empty row
        # no ID or ID not found
        if not row:
            row = []
            for i in range(len(h)):
                row.append('')

        # Load foreign keys into array
        fdata = dict()
        for fkey in mytable.foreign_keys:
            local = fkey.parent.name
            target = fkey.target_fullname.split('.')[0]
            ftable = eval('model.t_%s' % target)
            fselect = model.select([ftable])

            fdata[local] = dict()
            for i in meta.Session.execute(fselect).fetchall():
                fdata[local][i[0]] = i[1]

        rowArray = []
        for i in range(len(h)):
            # Do not display primary keys for editing
            if h[i] == pk.name:
                continue

            # Data is a foreign key. We want to use a drop down menu.
            choices = dict()
            if fdata.has_key(h[i]):
                # id:name
                for k,v in fdata[h[i]].items():
                    choices[k] = v

            try:
                myrow = [h[i],row[i],choices]
            except:
                myrow = [h[i],'',choices]
            rowArray.append(myrow)

        meta.Session.close()
        return rowArray

    def get_row(self,tablename,id):
        editable = request.params.get('insert')
        try:
            editable = int(editable)
        except:
            editable = 0

        id = int(id)
        mytable = self._get_table(tablename)
        h = mytable.columns.keys()
        pk = mytable.c.get(mytable.primary_key.columns.keys()[0])

        if id != 0:
            select = model.select([mytable], (pk == id))
            row = meta.Session.execute(select).fetchone()
        else:
            editable = 1
            row = []
            for i in range(len(h)):
                row.append('')

        fdata = dict()
        for fkey in mytable.foreign_keys:
            local = fkey.parent.name
            target = fkey.target_fullname.split('.')[0]
            ftable = eval('model.t_%s' % target)
            fselect = model.select([ftable])

            fdata[local] = dict()
            for i in meta.Session.execute(fselect).fetchall():
                fdata[local][i[0]] = i[1]

        rowString = ''
        for i in range(len(h)):
            if h[i] != pk.name:
                # Edit row
                if editable:
                    # Data is a foreign key. We want to use a drop down menu.
                    if fdata.has_key(h[i]):
                        rowString += '<td><select name="%s" id="%s">' % (h[i],h[i])
                        for k,v in fdata[h[i]].items():
                            if k == row[i]:
                                rowString += '<option value="%d" selected>%d: %s</option>' % (k,k,v)
                            else:
                                rowString += '<option value="%d">%d: %s</option>' % (k,k,v)
                        rowString += '</select></td>\n'
                    # Input box.
                    else:
                        if isinstance(row[i],basestring):
                            rowString += '<td><input type="text" name="%s" value="%s" /></td>\n' % (h[i],row[i])
                        elif isinstance(row[i],int):
                            rowString += '<td><input type="text" name="%s" value="%d" /></td>\n' % (h[i],row[i])
                        elif isinstance(row[i],float):
                            rowString += '<td><input type="text" name="%s" value="%f" /></td>\n' % (h[i],row[i])
                        else:
                            rowString += '<td><input type="text" name="%s" value="" /></td>\n' % (h[i])
                # Uneditable row
                else:
                    rowString += '<td>%s</td>' % row[i]

        meta.Session.close()
        return [rowString]

    @jsonify
    def save_row(self,tablename,id):
        value_arr = []
        for k,v in request.params.items():
            if v == '':
                pass
            elif k != 'table' and k != 'func' and k != 'pkid':
                value_arr.append('%s=\'%s\'' % (k,v))

        mytable = self._get_table(tablename)
        cmd = ''
        if int(id) > 0:
             pk = mytable.c.get(mytable.primary_key.columns.keys()[0])
             cmd = eval('mytable.update().where(pk == id).values(%s)' % ','.join(value_arr))
        else:
             cmd = eval('mytable.insert().values(%s)' % ','.join(value_arr))

        if cmd:
            log.debug('saving row: %s' % cmd)
            try:
                meta.Session.execute(cmd)
                meta.Session.commit()
            except sa_error.NoSuchColumnError, sa_error.NoSuchTableError:
                meta.Session.rollback()
                log.error('Insert/Update failed: %s' % cmd)
                return {'error':True, 'message':'No Such column or table. Check your WS call or talk to the site Administrator.' }
            except sa_error.IntegrityError:
                meta.Session.rollback()
                log.error('Insert/Update failed: %s' % cmd)
                message = 'The primary key already exists.'
                return {'error':True, 'message':message }
            except sa_error.DatabaseError:
                meta.Session.rollkack()
                log.error('Insert/Update failed: %s' % cmd)
                return {'error':True, 'message':'Database error.' }
            except:
                meta.Session.rollback()
                log.error('Insert/Update failed: %s' % cmd)
                return {'error':True, 'message':'Insert/Update failure due to unknown error.' }
            else:
                meta.Session.close()
        else:
            '%s is not an appropriate insert/update function' % func
            return

        meta.Session.close()
        return {'error':False, 'success':'Successfully saved row!'}

    def delete_row(self):
        tablename = request.params.get('table')
        id = int(request.params.get('id'))
        if isinstance(id,int) and isinstance(tablename,basestring):
            return self._delete_row(tablename,id)
        else:
            log.warn('Incorrect values: %s:%d' % (tablename,id))
            return [0]

    def unittest(self):
        return 'Function not implemented'

    def rnssummary(self):
         # @todo: redirect_to ('/user/resources')
         return

    def todo(self):
        return render('/admin/todo.mako')

    @jsonify
    def verifyadmin(self):
        userid = session.get('user_id','')
        password = request.params.get('auth', '').strip()

        if not (userid and password):
            c.message = "You must specify type the Administrator's password."
            return {'proceed':0, 'msg':c.message}

        # Query the database for the user
        u = meta.Session.query(model.User).filter(model.User.id == userid)
        if u.count() == 1 and u.one().password == encrypt(password,mysecret):
            self.verified = True
            return {'proceed':1}

        # Admin not authorized.
        c.message = 'Invalid Authorization. Please try again.'
        return {'proceed':0, 'msg':c.message}


    def changepassword(self):
        authid = session.get('user_id','')
        auth = request.params.get('auth','').strip()
        username = request.params.get('user','').strip()
        password = request.params.get('password','').strip()
        password_verify = request.params.get('password2','').strip()

        c.usernames = []
        for i in meta.Session.query(model.User):
            c.usernames.append(i.username)
        c.usernames.sort()

        if not len(request.params):
            return render('/admin/passwd.mako')

        if not (authid and auth):
            c.statusinfo = "You must specify type the Administrator's password."
            return render('/admin/passwd.mako')

        # Query the database for the user
        admin_auth = True
        u = meta.Session.query(model.User).filter(model.User.id == authid)
        if u.count() != 1 or u.one().password != encrypt(auth,mysecret):
            c.authinfo = "Administrator failed verification."
            admin_auth = False

        #Check for valid username and if the username exists in database
        user = meta.Session.query(model.User).filter(model.User.username == username)
        if user.count() != 1:
             c.statusinfo = 'Username %s does not exist.' % username
        elif len(password) < 8:
             c.statusinfo = 'Password must be at least 8 characters.'
        elif password != password_verify:
             c.statusinfo = 'Your passwords do not match. Please try it again.'
        elif encrypt(password,mysecret) == user.one().password:
             c.statusinfo = 'You cannot change to the same password. Please select another password.'
        elif admin_auth:
              # User data looks valid. Let's update the account
              user = user.one()
              user.password = encrypt(password,mysecret)
              try:
                    meta.Session.add(user)
                    meta.Session.commit()
              except Exception, e:
                    c.statusinfo = 'Couldn\'t update user (%s) password.' % username
                    log.error('%s %s',c.statusinfo,e)
              else:
                    meta.Session.close()
                    c.status = 1
                    c.statusinfo = 'Password for %s has been updated!' % username

        # User information encountered a problem. Collect the data and submit it back to the user.
        if not c.status:
            c.user = username
            if admin_auth:
                c.auth = auth
            else:
                c.password = password

        return render('/admin/passwd.mako')

    @jsonify
    def exportdb(self):
        log.info('Exporting database')

        db = dict()
        for t in meta.tables.keys():
            # Create an empty stub for each table.
            db[t] = {'columns':[], 'foreignkeys':{}, 'data':[]}

            try:
                mytable = eval('model.%s%s' % (t[0].upper(),t[1:]))
            except:
                continue

            if True:
                firstrun = True
                for i in meta.Session.query(mytable):
                    i = i.__dict__
                    row_arr = []
                    for k,j in i.items():
                        if k.startswith('_'):
                            continue

                        # Assemble column names
                        if firstrun:
                            db[t]['columns'].append(k)
                        # Assemble data
                        if isinstance(j,datetime):
                            row_arr.append(j.strftime('%m/%d/%Y %H:%M:%S'))
                        else:
                            row_arr.append(j)
                    db[t]['data'].append(row_arr)
                    firstrun = False
            try:
                pass
            except:
                log.error('Something crashed while exporting DB. Some data might be lost.')

        return db

    def exportdb_old(self):
        dbstring = '['
        for t in meta.tables.keys():
            try:
                mytable = self._get_table(t)
                columns = manager(mytable).keys()
                select = model.select([mytable])
                data = meta.Session.execute(select)
            except:
                continue

            data_arr = []
            for i in data.fetchall():
                 dstr = ''
                 for j in i:
                      if isinstance(j,int):
                            dstr += ',%d' % j
                      elif isinstance(j,float):
                            dstr += ',%f' % j
                      elif isinstance(j,basestring):
                            dstr += ',"' + j + '"'
                      else:
                            dstr += ','

                 data_arr.append(dstr[1:])

            dbstring += '\t{'
            dbstring += '\n'
            dbstring += '\t\t"tablename":"%s,"' % t
            dbstring += '\n'
            dbstring += '\t\t"columns":["%s"],' % '","'.join(columns)
            dbstring += '\n'
            #dbstring += '\t\t"rows":[%s]' % ',\n'.join(data_arr)
            dbstring += '\t\t"rows":[\n'
            for i in data_arr[:-1]:
                 dbstring += '\t\t\t[%s],' % i
                 dbstring += '\n'
            if len(data_arr) > 0:
                 dbstring += '\t\t\t[%s]' % data_arr[-1]
                 dbstring += '\n'
            dbstring += '\t\t]\n'

            dbstring += '\t},'
            dbstring += '\n'

        dbstring += ']'

        meta.Session.close()
        return dbstring

    # Helper functions start with '_'.
    def _delete_row(self,tablename,id):
        if not isinstance(id,int):
            try:
                id = int(id)
            except:
                log.error('Can\'t convert id to int: %s' % id)
                return [-1]

        try:
            mytable = self._get_table(tablename)
            pk = mytable.c.get(mytable.primary_key.columns.keys()[0])

            meta.Session.remove()

            delete = mytable.delete().where(pk == id)
            meta.Session.execute(delete)
            meta.Session.commit()
        except:
            meta.Session.rollback()
            log.error('Could not delete key')
            return [-1]
        else:
            meta.Session.flush()

        meta.Session.close()
        return [id]

    def _get_table(self,tablename):
         return eval('model.t_%s' % tablename)
