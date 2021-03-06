var multChoiceCreate = new MultChoiceCreate();

function openPopup() {
    document.getElementById("createQuestion").style.display = "block";
}

function closePopup() {
    document.getElementById("createQuestion").style.display = "none";
    document.getElementById("questionType").value = "Choose Question Type"
    document.getElementById("questionInputer").innerHTML = "";
}

function questionTypeUpdate() {
    var questionType = document.getElementById("questionType").value;
    var inputer = document.getElementById("questionInputer");

    if (questionType === "normal") {
        var htmlString = `<input type"text" id="mainQuestion" name="mainQuestion"><br>`;
        htmlString += `<input type="button" onclick="submitNormalQuestion()" value="Submit">`;
        inputer.innerHTML = htmlString;
    }
    else {
        multChoiceCreate = new MultChoiceCreate();
        var htmlString = `<p>Question: <input type="text" id="mainQuestion" name="mainQuestion"></p>`;
        htmlString += `<div id="multOptions"></div>`;

        htmlString += `<input type="button" onclick="addOption()" value="Add another option">`;
        htmlString += `<input type="button" onclick="submitMultiChoiceQuestion()" value="Submit">`;
        inputer.innerHTML = htmlString;

        multChoiceCreate.display(document.getElementById("multOptions"));
    }
        
}

function addOption() {
    multChoiceCreate.addOption();
    multChoiceCreate.display(document.getElementById("multOptions"));
}

function updateOption(id) {
    multChoiceCreate.updateOption(id, document.getElementById("option" + id.toString()).value);
}

function removeOption(id) {
    multChoiceCreate.removeOption(id);
    multChoiceCreate.display(document.getElementById("multOptions"));
}


function submitNormalQuestion() {
    if (/\S/.test(document.getElementById("mainQuestion").value)) {
        addNormalQuestion(document.getElementById("mainQuestion").value);
        onTemplateUpdate();
        closePopup();
    }
}

function addNormalQuestion(question) {
    var newQuestion = new Question("normal");
    newQuestion.setQuestion(question);
    questionTemplate.addQuestion(newQuestion);
}

function submitMultiChoiceQuestion() {
    var newQuestion = new Question("multichoice");
    if (/\S/.test(document.getElementById("mainQuestion").value)) {
        newQuestion.setQuestion(document.getElementById("mainQuestion").value);

        for (var i = 0; i < multChoiceCreate.options.length; i++) {
            newQuestion.addChoice(multChoiceCreate.options[i]);
        }

        questionTemplate.addQuestion(newQuestion);
        onTemplateUpdate();
        closePopup();
    }
}

