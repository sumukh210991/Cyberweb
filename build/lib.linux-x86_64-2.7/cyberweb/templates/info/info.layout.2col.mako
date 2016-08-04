<%inherit file="/2col-left.mako"/>

<%def name="headtags()">
</%def>

<%def name="footer()">
</%def>


<%def name="header()">
</%def>

<%def name="footer()">
</%def>

<%def name="col2main()">
    ${self.col2main()}
</%def>

<%def name="col2left()">
  <%
      # to add new navigation menu item just copy a line and modify the first action,
      # When adding a new menu column. place it in singular. (i.e. when adding users, add "user")
      # The code will check the plural as well
      menulist = {
                    'temp1': [],
                    'temp2': [],
                }
      a = ''
      for i in ['temp1','temp2']:
          if c.current_subnavtab.find(i) > -1 or c.current_subnavtab.find(i+'s') > -1:
              if i == 'account':
                  a = 'user'
              else:
                  a = i
      menu = menulist[a] if menulist.has_key(a) else dict()
  %>

  % for k,v in menu:
    <div class=leftnav>
		% if k == c.current_subnavtab:
            <a href="/exec/${k}" value="${k}" onClick="setvariable(this.value)";>${v}</a>
		% else:
            <a href="/exec/${k}" value="${k}" onClick="setvariable(this.value)";>${v}</a>
		% endif
    </div>
  % endfor
</%def>


<p>

${next.body()}
