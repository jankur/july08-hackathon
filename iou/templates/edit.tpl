<html>
<head>
  <title>IOU? - {{nickname}}</title>


<script language="JavaScript">
  <!-- Begin
  function addRow(id){
    var tbody = document.getElementById(id).getElementsByTagName("tbody")[0];
    var row = document.createElement("tr")

    var td1 = document.createElement("td")
    in1 = document.createElement("input")
    in1.setAttribute("name", "person")
    in1.setAttribute("id", "person")
    td1.appendChild(in1)

    var td2 = document.createElement("td")
    in2 = document.createElement("input")
    in2.setAttribute("name", "paid")
    in2.setAttribute("id", "paid")
    td2.appendChild(in2)

    var td3 = document.createElement("td")
    in3 = document.createElement("input")
    in3.setAttribute("name", "owed")
    in3.setAttribute("id", "owed")
    in3.setAttribute("value", "-1")
    td3.appendChild(in3)

    row.appendChild(td1);
    row.appendChild(td2);
    row.appendChild(td3);
    tbody.appendChild(row);
  }
</script>

</head>
<body>
  {% if errors %}
    <font color="red">
    <b>ERRORS</b><br/>
    {% for e in errors %}
      <li>{{e}}</li> 
    {% endfor %} 
    </font>
  {% endif %}
  Enter details of the transaction:
  <form action="/edit?tid={{transaction.key}}" method="post">
    Description:
      <input name="description"
             value="{{transaction.description|escape}}"><br/>
    Date: {{transaction.date|date:"d M Y"}}<br/>
    <a href="javascript:addRow('persons')">Add Participants</a>
    <table id="persons" cellspacing="0" border="1">
      <tbody>
        <tr>
          <td>Person</td><td>Amount Paid</td><td>Amount owed</td>
        </tr>
	{% for user in users %}
	<tr>
	  <td> <input name="person" value="{{user.user.email}}"> </td>
	  <td> <input name="paid" value="{{user.amount_paid}}"> </td>	
	  <td> <input name="owed" value="{{user.amount_owed}}"> </td>	
	</tr>
	{% endfor %}
      </tbody>
    </table>
    <center><input type="submit" value="Save"></center>
  </form>

</body>
</html>
