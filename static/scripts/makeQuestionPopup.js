var counter = 2; 

function openPopup() {
    document.getElementById("createQuestion").style.display = "block";
}

function closePopup() {
    document.getElementById("createQuestion").style.display = "none";
}

function questionTypeUpdate() {
    var questionType = document.getElementById("questionType").value;
    var inputer = document.getElementById("questionInputer");

    if (questionType === "normal") {
        var htmlString = `<input type"text" id="mainQuestion" name="mainQuestion"><br>`;
        htmlString += `<input type="button" onclick="submitNormalQuestion()" value="Submit">`;   
    }

    if (questionType === "multichoice") {
        var htmlString = `<input type"text" id="mainQuestion" name="mainQuestion"><br>`;
        htmlString += `<input type="button" onclick="addAdditionalChoice()" value="Add More Choices">`;
        htmlString += `<input type="button" onclick="submitMultiChoiceQuestion()" value="Submit">`;
        htmlString += `<input type"text" id="option1" name="option1"><br>`;
        htmlString += `<input type"text" id="option2" name="option2"><br>`;
    }
    inputer.innerHTML = htmlString;

}


function addNormalQuestion(question) {
    var newQuestion = new Question("normal");
    newQuestion.setQuestion(question);
    questionTemplate.addQuestion(newQuestion);
}

function submitNormalQuestion() {
    addNormalQuestion(document.getElementById("mainQuestion").value);
    onTemplateUpdate();
    closePopup();
}


function addMultiChoiceQuestion(question) {
    var newQuestion = new Question("multichoice");
    newQuestion.setQuestion(question);
    questionTemplate.addQuestion(newQuestion);
}

function submitMultiChoiceQuestion() {
    addMultiChoiceQuestion(document.getElementById("mainQuestion").value);
    onTemplateUpdate();
    closePopup();
}

function addAdditionalChoice() {
    counter += 1;
    var inputer = document.getElementById("questionInputer");
    inputer.innerHTML += `<input type"text" id="option"+counter name="option"><br>`;
}