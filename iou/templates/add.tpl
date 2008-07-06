<html>
<head>
  <title>IOU? - {{nickname}}</title>


<script language="JavaScript">
  <!-- Begin
  window.num_persons = 0;
  function addRow(id){
    window.num_persons += 1;
    var row_num = window.num_persons;
    var tbody = document.getElementById(id).getElementsByTagName("TBODY")[0];
    var row = document.createElement("TR")

    var td1 = document.createElement("TD")
    in1 = document.createElement("input")
    in1.setAttribute("name", "person" + row_num)
    in1.setAttribute("id", "person" + row_num)
    td1.appendChild(in1)

    var td2 = document.createElement("TD")
    in2 = document.createElement("input")
    in2.setAttribute("name", "paid" + row_num)
    in2.setAttribute("id", "paid" + row_num)
    td2.appendChild(in2)

    var td3 = document.createElement("TD")
    in3 = document.createElement("input")
    in3.setAttribute("name", "owes" + row_num)
    in3.setAttribute("id", "owes" + row_num)
    in3.setAttribute("value", "even")
    td3.appendChild(in3)

    row.appendChild(td1);
    row.appendChild(td2);
    row.appendChild(td3);
    tbody.appendChild(row);
  }
</script>

</head>
<body>
  Enter details of the transaction:
  <form action="/submit" method="post">
    <div>currency <input type="text" name="currency" size=3 value="USD"/>
    <div>tags <textarea name="description" rows=1 size=20 cols="20"></textarea></div>

    <a href="javascript:addRow('persons')">Add Participants</a>
    <table id="persons" cellspacing="0" border="1">
      <tbody>
        <tr>
          <td>Person</td><td>Amount Paid</td><td>Amount owed</td>
        </tr>
      </tbody>
    </table>


    <div><input type="submit" value="Enter Transaction"></div>
  </form>

</body>
</html>


