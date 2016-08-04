<%inherit file="/2col-left.mako"/>

<%def name="headtags()">
    ${next.headtags()}
</%def>

<%def name="header()">
</%def>

<%def name="footer()">
</%def>

<%def name="col2main()">
    ${next.col2main()}
</%def>

<%def name="col2left()">
  <%
      # to add new navigation menu item just copy a line and modify the first action,
      # When adding a new menu column. place it in singular. (i.e. when adding users, add "user")
      # The code will check the plural as well
      menulist = {
                    'user': [('user','CyberWeb User'),('cw_usergrouplist','User Group List'),('cw_usergroup','User Group'),('account','R&S Accounts'),('/admin/changepassword','Change password')],
                    'resource': [('resource','Resource')],
                    ###'service': [('service','Services'),('servicename','  Service Name'),('servicetype','  Service Type'), ('queueservice','QServ-old'),('queueingservice','Queueing Service'),('queuesystem','Queue Systems'),('queuetype','Queue Type'),   ('queueinfo','Queue Info')],
                    'service': [
				('service',         'Services'          ),
				('servicename',     'Service Name'      ),
				('servicetype',     'Service Type'      ), 
				('queueservice',    'QServ-old'         ),
				('queueingservice', 'Queueing Service'  ),
				('queuesystem',     'Queue Systems'     ),
				('queuetype',       'Queue Type'        ),   
				('queueinfo',       'Queue Info'        )
				],
                    'job': [('job','Manage User Jobs'),('task','Manage User Tasks')],
                    'message': [('messagetype','Message Type'),('message','Message')],
                }
      a = ''
      arr = menulist.keys()
      # Append our 1-off cass 'account'
      arr.append('account')
      for i in arr:
          if c.current_subnavtab.find(i) > -1 or c.current_subnavtab.find(i+'s') > -1:
              if i == 'account':
                  a = 'user'
              else:
                  a = i
      menu = menulist[a] if menulist.has_key(a) else dict()
  %>

  % for k,v in menu:
    <div class=leftnav>
	    <%
		  link = k if k.startswith('/') else '/admin/table/' + k
		%>
        <a href="${link}" value="${k}" >${v}</a>
    </div>
  % endfor
</%def>
