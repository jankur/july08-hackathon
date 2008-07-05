<html>
<head>
  <title>IOU? - {{username}}</title>
</head>
<body>
  List of ALL transactions:
  <ul>
  {% for t in transactions %}
    <li><b>{{ t.date|date:"d M Y "}}</b>:
    {{t.description}}</li>
  {% endfor %}
  </ul> 
</body>
</html>
