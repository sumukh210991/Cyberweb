<%inherit file="/1col.mako"/>

<%def name="col1main()">
<h3>${c.title}</h3>
<p>

<h2>GCEM Simulation Manager: A Workflow for building and running GCEM Ocean Models</h2>
<ul>
<li>CREATE:  build a new Simulation, and save (can be reused/copied for next job) </li>
<li>EXECUTE:  select [existing simulation  OR create new (redirect)], set params for running and submit job to queue </li>
<li>MONITOR: job monitor/interactive/view interim results/cancel </li>
<li>ANALYZE: view perf and other data. Save/Del/Cancel (if running)/resub </li>
</ul>
</%def>

