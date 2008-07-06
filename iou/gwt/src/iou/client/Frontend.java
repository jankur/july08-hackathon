package iou.client;

import com.google.gwt.core.client.EntryPoint;
import com.google.gwt.json.client.JSONArray;
import com.google.gwt.json.client.JSONException;
import com.google.gwt.json.client.JSONObject;
import com.google.gwt.json.client.JSONParser;
import com.google.gwt.json.client.JSONString;
import com.google.gwt.json.client.JSONValue;
import com.google.gwt.user.client.HTTPRequest;
import com.google.gwt.user.client.ResponseTextHandler;
import com.google.gwt.user.client.ui.FlexTable;
import com.google.gwt.user.client.ui.Label;
import com.google.gwt.user.client.ui.RootPanel;
import com.google.gwt.user.client.ui.Widget;

class JSONHandler implements ResponseTextHandler {
  private static String LINK_PREFIX = "/edit?tid=";
  private FlexTable widget;

  public JSONHandler(FlexTable widget) {
    this.widget = widget;
  }

  public void onCompletion(String responseText) {
    try {
      JSONArray transactions = JSONParser.parse(responseText).isArray();
      if (transactions == null) {
	displayError();
      } else {
	displayTransactions(transactions);
      }
    } catch (JSONException e) {
      // TODO
    }
  }

  private void displayError() {
    // TODO
  }

  private void displayTransactions(JSONArray transactions) {
    widget.setVisible(true);
    widget.setBorderWidth(1);
    for (int i = 0; i < transactions.size(); ++i) {
      JSONObject t = transactions.get(i).isObject();
      if (t == null) {
	displayError();
      } else {
	displayTransaction(t);
      }
    }
  }

  private void displayTransaction(JSONObject t) {
    // TODO: Handle nulls from t.get()
    int num_rows = widget.getRowCount();
    String url = "/edit?tid=" + t.get("tid").isString().stringValue();
    String date = t.get("date").isString().stringValue();
    String desc = t.get("description").isString().stringValue();
    
    widget.setText(num_rows, 0, date);
    widget.setHTML(num_rows, 1, "<a href=\"" + url + "\">" + desc +
                                "</a>");
  }
}

public class Frontend implements EntryPoint {
  private static String JSON_URL = "/json";
  private FlexTable transactionTable = new FlexTable();


  public void onModuleLoad() {
    if (!HTTPRequest.asyncGet(JSON_URL, new JSONHandler(transactionTable))) {
      final Label label = new Label();
      label.setText("Are you doing hanky panky?");
      RootPanel.get("slot").add(label);
      return;
    }
    RootPanel.get("slot").add(transactionTable);
  }
}
