/* 
ссылка на таблицу: 
https://docs.google.com/spreadsheets/d/1Ro66LHo8sWzHjmwHoEGXe-xdUFrVu89qIO2gVcFgzU0/edit?usp=sharing

формулы: 
=importxml(A*;"//h1")
=IMAGE(IMPORTXML(A*;"//img/@src"))
=importxml(A*;"//meta[@name='description']/@content")
*/


function MyFunction() {
 
    var ss = SpreadsheetApp.getActiveSpreadsheet();
    var sheet = ss.getSheetByName('google');
    var values = sheet.getDataRange().getValues();
 
    for (var i = 1; i < values.length; i++) {
        var url = values[i][0];
        var response = UrlFetchApp.fetch(url, {
            'muteHttpExceptions': true,
            'validateHttpsCertificates': false,
        });
 
        var responseCode = response.getResponseCode();
        var content = response.getContentText();
 
        if (responseCode === 200) {
            var title = content.match(/title>(.*?)\</)[1];
            sheet.getRange(i + 1, 2).setValue(title);
            }
    }
}
