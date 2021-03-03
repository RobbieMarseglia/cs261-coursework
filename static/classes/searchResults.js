class SearchResults {
    constructor() {
        this.results = [];
    }

    setResults(results) {
        this.results = results;
    }

    getResultString(id) {
        return `{"date_time":` + this.results[id]["date_time"] + `, "title":` + this.results[id]["title"] + `}`;
    }

    getHTMLString() {
        var HTMLString = "";
        var loopString = "";

        for (var i = 0; i < this.results.length; i++) {
            loopString = `<div class="searchResult" onclick="selectResult(` + i.toString() + `)">`
            loopString += `<p>Title: ` + this.results[i]["title"] + `</p>`;
            loopString += `<p>Start Time: ` + this.results[i]["date_time"] + `</p></div>`;

            HTMLString += loopString;
        }

        return HTMLString;
    }

    display(node) {
        node.innerHTML = this.getHTMLString();
    }
}