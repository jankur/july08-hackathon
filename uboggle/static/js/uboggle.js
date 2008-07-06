var words = ["foo", "bar", "baz"];

function addWordToList() {
  var new_word = $("#new_word").val();
  if (new_word.length < 3) {
    $.jGrowl("Words should be at least 3 characters!",
             {life: 2000});
    $("#new_word").css("border", "thin solid red");
    $("#new_word").val("");
    return;
  }

  // make sure word has not already been entered
  if (words.indexOf(new_word) != -1) {
    $.jGrowl("You have already entered this word. Try again!",
             {life: 2000});
    $("#new_word").css("border", "thin solid red");
    $("#new_word").val("");
    return;
  }

  // make sure it is a valid word on the board
  words.push(new_word);
  $("#input_words p").append(new_word + ", ");
  $("#new_word").val("");
}

function initialize() {
  $("#submit_new_word").click(addWordToList);
  $("#countdown").countdown({until: 120, format: 'S', onExpiry: gameOver});
}

function gameOver() {
  $.post("/testjson", {'words': words}, function (data) {alert('Data!');}, "json");
}

google.setOnLoadCallback(initialize);
