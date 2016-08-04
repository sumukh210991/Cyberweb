<%inherit file="/1col.mako"/>

<%def name="col1main()">
<style type="text/css">
    table, td, th
    {
    width:600px;
    border:1px solid black;
    }
    td
    {
    height:400px;
    vertical-align:top;
    }

    #jobs table, #jobs th, #jobs td
    {
    width:600px;
    border:1px solid black;
    }
    #jobs th
    {
    height:200px;
    vertical-align:top;
    }
    #jobs td
    {
    height:200px;
    vertical-align:top;
    }
</style>

<h3>${c.title}</h3>
<p>


<blockquote>
   <table id="jobs">
   <tr><td>
   list all jobs in top panel job status/progress
   </td></tr>
   </table>
</blockquote>
<blockquote>
   <table style="vertical:600px">
   <tr><td>
   <p> on selection of job in panel above, display job details
   <p>interact with job (cancel)
   <p>view interim results --> redirect to analyze 
   </td></tr>
   </table>
</blockquote>

</%def>

