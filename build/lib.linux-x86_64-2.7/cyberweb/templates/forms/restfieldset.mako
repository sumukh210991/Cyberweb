<%inherit file="/layout.mako"/>

<%!
from formalchemy.ext.pylons.controller import model_url
from pylons import url
%>

<%def name="headtags()">
    <title>
    ${collection_name.title()}
    </title>
    
</%def>

<%def name="header()"> 
</%def>

<%def name="footer()">
</%def>

<%def name="h1(title, href=None)">
    <h1 id="header" class="ui-widget-header ui-corner-all">
      %if breadcrumb:
        <div class="breadcrumb">
         /${'/'.join([u and '<a href="%s">%s</a>' % (u,n.lower()) or n.lower() for u,n in breadcrumb])|n} 
        </div>
      %endif
      %if href:
        <a href="${href}">${title.title()}</a>
      %else:
        ${title.title()}
      %endif
    </h1>
</%def>
<%def name="buttons()">
    <p class="fa_field">
      <a class="ui-widget-header ui-widget-link ui-widget-button ui-corner-all" href="#">
        <input type="submit" value="${F_('Save')}" />
      </a>
      <a class="ui-widget-header ui-widget-link ui-corner-all" href="${model_url(collection_name)}">
        <span class="ui-icon ui-icon-circle-arrow-w"></span>
        ${F_('Cancel')}
      </a>
    </p>
</%def>
<div id="mainContent">
	<div id="leftMenuItems" class="ui-admin ui-widget">
	  %if isinstance(models, dict):
	    %for name in sorted(models):
	      <p>
	        <a class="ui-state-default ui-corner-all" href="${models[name]}">${name}</a>
	      </p>
	    %endfor
			<p>
				<a class="ui-state-default ui-corner-all" href="/newadmin/getResoruceServiceList">Resource Service Lists</a>
			</p>
	  %elif is_grid:
	    ${h1(model_name)}
	    <div class="ui-pager">
	      ${pager|n}
	    </div>
	    <table class="layout-grid">
	    ${fs.render()|n}
	    </table>
	    <p>
	      <a class="ui-widget-header ui-widget-link ui-corner-all" href="${model_url('new_%s' % member_name)}">
	          <span class="ui-icon ui-icon-circle-plus"></span>
	          ${F_('New')} ${model_name}
	      </a>
	    </p>
	  %else:
	    ${h1(model_name, href=model_url(collection_name))}
	    %if action == 'show':
	      <table>
	        ${fs.render()|n}
	      </table>
	      <p class="fa_field">
	        <a class="ui-widget-header ui-widget-link ui-corner-all" href="${model_url('edit_%s' % member_name, id=id)}">
	          <span class="ui-icon ui-icon-pencil"></span>
	          ${F_('Edit')}
	        </a>
	      </p>
	    %elif action == 'edit':
	      <form action="${model_url(member_name, id=id)}" method="POST" enctype="multipart/form-data">
	        ${fs.render()|n}
	        <input type="hidden" name="_method" value="PUT" />
	        ${buttons()}
	      </form>
	    %else:
	      <form action="${model_url(collection_name)}" method="POST" enctype="multipart/form-data">
	        ${fs.render()|n}
	        ${buttons()}
	      </form>
	    %endif
	  %endif
	</div>
</div>
<script type="text/javascript">
  var icons = document.getElementsByClassName('ui-icon')
  for (var i = 0; i < icons.length-1; i++) {
    icons[i].setAttribute('value', ' ');
  } 
</script>
