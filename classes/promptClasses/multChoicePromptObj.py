from .generalPromptObj import GeneralPrompt

class MultChoicePrompt(GeneralPrompt):

    def __init__(self, hostID, meetingID, promptText, multChoices = list()):
        super().__init__(hostID, meetingID, promptText)
        self.multChoices = multChoices
    
    def getMultChoices(self):
        return self.multChoices

    def addChoice(self,choice):
        self.multChoices.append(choice)
    
    def removeChoice(self,choice):
        self.multChoices.remove(choice)
        