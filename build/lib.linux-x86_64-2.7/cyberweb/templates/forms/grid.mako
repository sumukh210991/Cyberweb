<thead>
  <tr>
    %for field in collection.render_fields.itervalues():
      <th>${F_(field.label_text or collection.prettify(field.key))|h}</th>
    %endfor
  </tr>
</thead>

<tbody>
%for i, row in enumerate(collection.rows):
  <% collection._set_active(row) %>
  <% row_errors = collection.get_errors(row) %>
  <tr class="${i % 2 and 'odd' or 'even'}">
  %for field in collection.render_fields.itervalues():
    <td>
      ${field.render()|n}
      %for error in row_errors.get(field, []):
      <span class="grid_error">${error}</span>
      %endfor
    </td>
  %endfor
  </tr>
%endfor
</tbody>