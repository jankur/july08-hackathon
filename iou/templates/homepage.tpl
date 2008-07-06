<html>
<head>
  <title>IOU? - {{username}}</title>
</head>
<body>
  <a href="/add">Add a transaction</a>
  <p/>
  List of ALL transactions:
  <ul>
  {% for t in transactions %}
    <li>
      <a href="/edit?tid={{t.key}}"><b>{{ t.date|date:"d M Y "}}</b>:
       {{t.description}}</a>
    </li>
  {% endfor %}
  </ul> 
</body>
</html>
