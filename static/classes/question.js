class Question {
    constructor(type) {
        // Types can be: "normal"
        this.type = type;
        this.question = "";
        // If the question is "multchoice" then the multiple choices are added 
        // to this list below. Note that all multiple choice questions must have 4 choices
        this.choice_list = [];
    }

    setQuestion(question) {
        this.question = question;
    }

    addChoice(choice) {
        this.choice_list.push(choice);
    }

    getJSONString() {
        var JSONString = `{"question":"` + this.question + `", "type":"` + this.type + `", "options":[`;

        for (var i = 0; i < this.choice_list.length; i++) {
            JSONString += `"` + this.choice_list[i] + `", `;
        }

        if (this.choice_list.length > 0) {
            JSONString = JSONString.substring(0, JSONString.length - 2);
        }

        return JSONString + "]}"
    }

}