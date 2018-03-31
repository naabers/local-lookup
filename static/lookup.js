// document.addEventListener('paste', function (e) {
// 	lookupCharacters()
// }, false);

function getCommaSeparatedCharacters() {
    var characters = ""
    var inputText = document.getElementById('sendtext').value;
    var lines = inputText.split('\n');
    for(var i = 0;i < lines.length;i++){
        if(lines[i].trim().length > 0) {
            if(characters != "") {
                characters += ","
            }
            console.log(lines[i].trim())
            characters += lines[i].trim()
        }
    }
    return characters
}

function updateResults(jsonResponse) {
    var resultsText = ""

    for(var i = 0;i < jsonResponse.length;i++){
        killmailInfo = jsonResponse[i]
        resultsText += killmailInfo['character_name'] + "\n"
        resultsText += killmailInfo['killmail_time'] + "\n"
        resultsText += killmailInfo['ship_name'] + "\n"
        resultsText += killmailInfo['item_discovered'] + "\n"
        resultsText += "\n"
    }
    if(resultsText == "") {
        resultsText = "Local appears to be safe"
        console.log(resultsText)
    }
    console.log(resultsText)
    document.getElementById('results').innerHTML = resultsText
}

function lookupCharacters() {
    var characterString = getCommaSeparatedCharacters()
    if(characterString == "") {
        document.getElementById('results').innerHTML = "Invalid character input..."
        console.log("oops")
    }

    document.getElementById('results').innerHTML = "Processing..."
    console.log("processing")

    var url = "http://127.0.0.1:5000/characters/information/" + characterString

    fetch(url)
        .then(function(response) {
            return response.json()
        })
        .then(function(jsonResponse) {
            updateResults(jsonResponse)
        });
}
