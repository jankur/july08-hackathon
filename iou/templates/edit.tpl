<html>
<head>
  <title>IOU? - {{nickname}}</title>


<script language="JavaScript">
  <!-- Begin
  window.num_persons = {{num_users}};
  function addRow(id){
    var row_num = window.num_persons;
    var tbody = document.getElementById(id).getElementsByTagName("tbody")[0];
    var row = document.createElement("tr")

    var td1 = document.createElement("td")
    in1 = document.createElement("input")
    in1.setAttribute("name", "person" + row_num)
    in1.setAttribute("id", "person" + row_num)
    td1.appendChild(in1)

    var td2 = document.createElement("td")
    in2 = document.createElement("input")
    in2.setAttribute("name", "paid" + row_num)
    in2.setAttribute("id", "paid" + row_num)
    td2.appendChild(in2)

    var td3 = document.createElement("td")
    in3 = document.createElement("input")
    in3.setAttribute("name", "owed" + row_num)
    in3.setAttribute("id", "owed" + row_num)
    in3.setAttribute("value", "even")
    td3.appendChild(in3)

    row.appendChild(td1);
    row.appendChild(td2);
    row.appendChild(td3);
    tbody.appendChild(row);
    window.num_persons += 1;
  }
</script>

</head>
<body>
  Enter details of the transaction:
  <form action="/edit?tid={{transaction.key}}" method="post">
    Description:
      <input name="description"
             value="{{transaction.description|escape}}">

    <a href="javascript:addRow('persons')">Add Participants</a>
    <table id="persons" cellspacing="0" border="1">
      <tbody>
        <tr>
          <td>Person</td><td>Amount Paid</td><td>Amount owed</td>
        </tr>
	{% for user in users %}
	<tr>
	  <td>
	    <input name="person{{forloop.counter0}}"
                   value="{{user.user.nickname}}">
	  </td>
	  <td>
	    <input name="paid{{forloop.counter0}}" value="{{user.amount_paid}}">
	  </td>	
	  <td>
	    <input name="owed{{forloop.counter0}}" value="{{user.amount_owed}}">
	  </td>	
	</tr>
	{% endfor %}
      </tbody>
    </table>
    <center><input type="submit" value="Save"></center>
  </form>

</body>
</html>
