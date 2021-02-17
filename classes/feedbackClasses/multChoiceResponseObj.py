import responseObj

class MultChoiceResponse(responseObj.Response):

    def __init__(self, anonFlag, attendeeID, responsePrompt, responseChoice):
        super().__init__(anonFlag, attendeeID, responsePrompt)
        self.responseChoice = responseChoice
    
    def getResponseChoice(self):
        return self.responseChoice
