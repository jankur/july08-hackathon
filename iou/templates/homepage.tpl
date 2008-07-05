<html>
<head>
  <title>IOU? - {{username}}</title>
</head>
<body>
  List of ALL transactions:
  <ul>
  {% for t in transactions %}
    <li>
      <a href="/?tid={{t.key}}"><b>{{ t.date|date:"d M Y "}}</b>:
       {{t.description}}</a>
    </li>
  {% endfor %}
  </ul> 
</body>
</html>
