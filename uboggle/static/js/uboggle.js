var words = ["foo", "bar", "baz"];

function addWordToList() {
  var new_word = $("#new_word").val();
  words.push(new_word);
  $("#input_words p").append(new_word + ", ");
  $("#new_word").val("");
}

function initialize() {
  $("#submit_new_word").click(addWordToList);
  $("#countdown").countdown({until: 120, format: 'S', onExpiry: gameOver});
}

function gameOver() {
  $.post("/testjson", {'words': words}, function (data) {}, "json");
}

google.setOnLoadCallback(initialize);
