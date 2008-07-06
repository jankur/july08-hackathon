var words = [];

function existsOnBoard(new_word) {
  // make sure it is a valid word on the board
  index = lower_case_board.indexOf(new_word.charAt(0));
  if (index == -1) {
    $.jGrowl("This word is not on the board!",
             {life: 2000});
    $("#new_word").css("border", "thin solid red");
    $("#new_word").val("");
    return false;
  }
  x = index / 4 | 0; // convert to int
  y = index % 4;
  alive = true;
  for(i = 1; i < new_word.length && alive; i++) {
    // there might be multiple places where this letter is
    var foundIndices = []
    var nIndex = lower_case_board.indexOf(new_word.charAt(i));
    while (nIndex != -1) {
      foundIndices.push(nIndex);
      nIndex = lower_case_board.indexOf(new_word.charAt(i), ++nIndex);
    }

    for(j = 0; j < foundIndices.length && alive; j++) {
      if (j == -1) {
        alive = false;
        break;
      }
      nX = j / 4 | 0; // convert to int
      nY = j % 4;
      if((x > 0 && nX == x-1 && nY == y) ||
         (x < 3 && nX == x+1 && nY == y) ||
         (y > 0 && nX == x && nY == y-1) ||
         (y < 3 && nX == x && nY == y+1) ||
         (x > 0 && y > 0 && nX == x-1 && nY == y-1) ||
         (x < 3 && y < 3 && nX == x+1 && nY == y+1) ||
         (x > 0 && y < 3 && nX == x-1 && nY == y+1) ||
         (x < 3 && y > 0 && nX == x+1 && nY == y-1)) {
        x = nX;
        y = nY;
      }
      else {
        $.jGrowl(nX + "," + nY + " | " + x + "," + y);
        $.jGrowl(lower_case_board[nIndex] + "," +
                 lower_case_board[index] + "," +
                 new_word[i] + "," + new_word[i-1]);
        alive = false;
        break;
      }
    }
  }
  if(!alive) {
    $.jGrowl("This word is not on the board!",
             {life: 2000});
    $("#new_word").css("border", "thin solid red");
    $("#new_word").val("");
    return;
  }
}

function addWordToList() {
  var new_word = $("#new_word").val().toLowerCase();

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

  alive = true;
  for(i = 0; i < new_word.length && alive; i++) {
    if (lower_case_board.indexOf(new_word.charAt(i)) == -1) {
      alive = false;
      break;
    }
  }
  if(!alive) {
    $.jGrowl("This word is not on the board!",
             {life: 2000});
    $("#new_word").css("border", "thin solid red");
    $("#new_word").val("");
    return;
  }

  words.push(new_word);
  $("#input_words p").append(new_word + ", ");
  $("#new_word").val("");
}

function initialize() {
  $("#countdown").countdown({until: 120, format: 'S', onExpiry: gameOver});
}

function gameOver() {
  $.post("/testjson", {'words': words}, function (data) {alert('Data!');}, "json");
}

google.setOnLoadCallback(initialize);
