## index.html

## Body
<%
    # Python code to manipulate file/directory names for javascript var names
	import re
	varre = re.compile("\.|\(|\)| ")
	listvar = {}
	dirvar = {}
	for a in c.listing:
		listvar[a] = varre.subn('',a)[0]
		dirvar[a] = 1 if a[-5:] == '(dir)' else 0
%>

<div id="sortable">
	<ol>
		<li><div id="parentfolder">Parent Folder</div></li>
		<li><div id="draggable">DRAG ME</div></li>
% for a in c.listing:
		<li><div id="${listvar[a]}" class="fileitem">${a}</div></li>
    % if dirvar[a] == 1:
	    <li><div id="${listvar[a]}" class="diritem">${a}</div></li>
    % endif
% endfor
	</ol>	
</div>