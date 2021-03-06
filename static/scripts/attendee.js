var hostQuestions = new HostQuestions();

socket.on("connection_response", function(data) {
    if (data == "connected") {
        socket.emit("connect_as_attendee", {"code" : meetingcode});
    }
});

socket.on("meeting_ended", function(data) {
    console.log(window.location.href);
    var sections = window.location.href.split("/")
    var counter = 0;
    var newURL = "";

    while (counter < sections.length && sections[counter] !== "meeting") {
        newURL += sections[counter] + "/";
        counter += 1
    }

    window.location.href = newURL + "meetingend";
});

socket.on("meeting_details", function(data) {
    if (data["connection_status"] == "connected") {
        document.getElementById("connection_status").innerHTML = "Connected to room " + meetingcode.toString();
        document.getElementById("meeting_title").innerHTML = data["title"];
        
        hostQuestions.fromJSON(data["template"]);
        hostQuestions.displayTemplate(document.getElementById("hostQuestions"));
    } else {
        document.getElementById("connection_status").innerHTML = "Connection failed";
    }
});

socket.on("template_update", function(data) {
    console.log(data);
    hostQuestions.fromJSON(data["template"]);
    hostQuestions.displayTemplate(document.getElementById("hostQuestions"));
});

function sendGeneralFeedback() {
    socket.emit("general_feedback", {"feedback":document.getElementById("generalFeedbackInput").value});
    document.getElementById("generalFeedbackInput").value = "";
}

function sendErrorFeedback() {
    socket.emit("error_feedback", {"error":document.getElementById("errorFeedbackInput").value});
    document.getElementById("errorFeedbackInput").value = "";
}

function sendQuestionAnswer(id) {
    var answer = document.getElementById("question_" + id).value;
    var question = hostQuestions.template.questions[Number(id)].getJSONString();
    socket.emit("question_response", {"question":question, "answer":answer});
}

function sendVeryConfusedEmoji() {
    socket.emit("emoji_response", { "emoji": -1.0 });
}

function sendSlightlyConfusedEmoji() {
    socket.emit("emoji_response", { "emoji": -0.5 });
}

function sendNeutralEmoji() {
    socket.emit("emoji_response", { "emoji": 0.0 });
}

function sendSlightlyHappyEmoji() {
    socket.emit("emoji_response", { "emoji": 0.5 });
}

function sendVeryHappyEmoji() {
    socket.emit("emoji_response", { "emoji": 1.0 });
}

function sendMultChoiceAns(question, option) {
    var question = hostQuestions.template.questions[Number(question)];
    var answer = question.choice_list[Number(option)]
    socket.emit("mult_choice_response", {"question":question.getJSONString(), "answer":answer});
}