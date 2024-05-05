#zu dokuzwecken

function createFormQuestions() {

  var ssId  ='1xYOH5jUYsP79SH8TD1ObDgfA6s4xnk9osLhg_JkvlrU'
  var spreadsheet = SpreadsheetApp.openById(ssId);
  Logger.log('Spreadsheet Title: ' + spreadsheet.getName());
  var formId = '1MIQDtTRjEgPzew0oMZ5qyAnO99QmPmpRFyujmdUDBDw';
  var form = FormApp.openById(formId);

  var sheet = spreadsheet.getSheetByName('Tabellenblatt1');
  if (!sheet) {
    Logger.log('Sheet not found. Check the sheet name.');
    return;
  }
  var range = sheet.getRange(2, 1, sheet.getLastRow()-1, 2);
  var data = range.getValues();

  data.forEach(function(row) {
    var itemA = row[0];
    var itemB = row[1] + '.';
    var question = form.addMultipleChoiceItem();
    question.setTitle('Welche Betreffzeile gefällt Ihnen besser?')
            .setChoices([
                question.createChoice(itemA),
                question.createChoice(itemB)
            ]);
  });
}
