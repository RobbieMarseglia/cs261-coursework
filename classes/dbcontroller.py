import datetime
import hashlib
import secrets
import sqlite3
import string
import time

from .feedbackClasses import *

class DBController:

    def __init__(self):
        # Establishes DB connection and a cursor
        try:
            self.conn = sqlite3.connect('live_feedback.db')
            self.cursor = self.conn.cursor()
        except sqlite3.Error as error:
            print("Failed to open database connection", error)

    def close(self):
        # Closes connection to database
        self.conn.close()

    def __insert_feedback(self, meeting, f_type):
        # Helper function to insert a general feedback type
        try:
            self.cursor.execute("INSERT INTO feedback VALUES (NULL, :m, :t)",{'m':meeting, 't':f_type})
            self.cursor.execute("SELECT last_insert_rowid()")
            return self.cursor.fetchone()[0]
        except sqlite3.Error as error:
            return error

    def insert_error(self, error):
        """Stores feedback of type: Error

        Parameters:
            error {ErrorFeedback} -- ErrorFeedback object containing details of error

        """
        meeting = error.get_meeting()
        err_type = error.get_error_type()
        err_msg = error.get_error_message()

        feedback = self.__insert_feedback(meeting, "error")

        if type(feedback) is int:
            try:
                self.cursor.execute("INSERT INTO errors VALUES (:f, :t, :m)",{'f':feedback, 't':err_type, 'm':err_msg})
                self.conn.commit()
            except sqlite3.Error as err:
                print("Error inserting into table errors:", err)
                self.conn.rollback()
        else:
            print("Error inserting into table feedback:", feedback)
            self.conn.rollback()

    def insert_question(self, question):
        """Stores feedback of type: Question

        Parameters:
            question {QuestionFeedback} -- QuestionFeedback object containing details of question

        """
        meeting = question.get_meeting()
        qstn_msg = question.get_question_text()

        feedback = self.__insert_feedback(meeting, "question")

        if type(feedback) is int:
            try:
                self.cursor.execute("INSERT INTO questions VALUES (:f, :m)",{'f':feedback, 'm':qstn_msg})
                self.conn.commit()
            except sqlite3.Error as error:
                print("Error inserting into table questions:", error)
                self.conn.rollback()
        else:
            print("Error inserting into table feedback:", feedback)
            self.conn.rollback()

    def __insert_general_mood(self, feedback, mood_type, score, time, average):
        # Helper function to insert a general mood feedback
        try:
            self.cursor.execute("INSERT INTO moods VALUES (NULL, :f, :t, :s, :l, :a)",{'f':feedback, 't':mood_type, 's':score, 'l':time, 'a':average})
            self.cursor.execute("SELECT last_insert_rowid()")
            return self.cursor.fetchone()[0]
        except sqlite3.Error as error:
            return error

    def insert_mood(self, mood):
        """Stores feedback of type: Mood

        Parameters:
            mood {emojiMoodObj/textMoodObj} -- Emoji or Text Mood object containing relevant details

        """
        cancel = False
        meeting = mood.get_meeting()
        mood_type = mood.get_mood_type()
        score = mood.get_mood_score()
        current_time = datetime.datetime.strptime(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(mood.get_mood_time())), "%Y-%m-%d %H:%M:%S")
        current_avg = mood.get_current_mood_avg()
        try:
            self.cursor.execute("SELECT date_time FROM meetings WHERE meetingid = :m",{'m':meeting})
            start_time = datetime.datetime.strptime(self.cursor.fetchone()[0], "%Y-%m-%d %H:%M:%S")
            meeting_time = current_time - start_time
        except sqlite3.Error as error:
            print("Error selecting meetingid from table meetings:",error)
            cancel = True
        if not cancel:
            if mood_type == "text" or mood_type == "emoji":
                feedback = self.__insert_feedback(meeting, "mood")
                if type(feedback) is int:
                    mood_ID = self.__insert_general_mood(feedback, mood_type, score, str(meeting_time), current_avg)
                    if type(mood_ID) is int:
                        if mood_type == "text":
                            data = mood.get_mood_text()
                        else:
                            data = mood.get_mood_emoji()
                        try:
                            self.cursor.execute("INSERT INTO " + mood_type + "_moods VALUES (:m, :t)",{'m':mood_ID, 't':data})
                            self.conn.commit()
                        except sqlite3.Error as error:
                            print("Error inserting into table " + mood_type + "_moods:", error)
                            self.conn.rollback()
                    else:
                        print("Error inserting into table moods:", mood_ID)
                        self.conn.rollback()
                else:
                    print("Error inserting into table feedback:", feedback)
                    self.conn.rollback()
            else:
                print("Invalid mood type:", mood_type)

    def __insert_general_response(self, feedback, response_type, prompt):
        # Helper function to insert a general response feedback
        try:
            self.cursor.execute("INSERT INTO responses VALUES (NULL, :f, :t, :p)",{'f':feedback, 't':response_type, 'p':prompt})
            self.cursor.execute("SELECT last_insert_rowid()")
            return self.cursor.fetchone()[0]
        except sqlite3.Error as error:
            return error

    def insert_response(self, response):
        """Stores feedback of type: Response

        Parameters:
            response {emojiResponseObj/multChoiceResponseObj/testResponseObj} -- Emoji, Multiple Choice, or Text Response object containing relevant details

        """
        meeting = response.get_meeting()
        response_type = response.get_response_type()
        prompt = response.get_response_prompt()

        if response_type == "emoji" or response_type == "text" or response_type == "multchoice":
            feedback = self.__insert_feedback(meeting, "response")
            if type(feedback) is int:
                response_ID = self.__insert_general_response(feedback, response_type, prompt)
                if type(response_ID) is int:
                    if response_type == "emoji":
                        data = response.get_response_emoji()
                    elif response_type == "text":
                        data = response.get_response_text()
                    else:
                        data = response.get_response_answer()
                        response_type = "mult_choice"
                    try:
                        self.cursor.execute("INSERT INTO " + response_type + "_responses VALUES (:r, :d)",{'r':response_ID, 'd':data})
                        self.conn.commit()
                    except sqlite3.Error as error:
                        print("Error inserting into table " + response_type +"_responses:", error)
                        self.conn.rollback()
                else:
                    print("Error inserting into table responses:", response_ID)
                    self.conn.rollback()
            else:
                print("Error inserting into table feedback:", feedback)
                self.conn.rollback()
        else:
            print("Invalid response type:", response_type)

    def unique_token(self, token):
        """Determines if token is unique

        Parameters:
            token {int} -- Token to check uniqueness of

        Returns:
            True/False {boolean} -- Indicates whether token is unique
        """
        try:
            self.cursor.execute("SELECT meetingid FROM meetings WHERE meetingid == :m",{'m':token})
            if self.cursor.fetchone() is None:
                return True
            return False
        except sqlite3.Error as error:
            print("Error selecting meetingid from table meetings:",error)
            return False

    def insert_meeting(self, meeting_token, host_token, title):
        """Stores newly created meeting

        Parameters:
            meeting_token {int} -- Identifier for the given meeting
            host_token {string} -- Host's curent access token
            title {string} -- Stores meeting title in key 'name' and meeting password in key 'keyword'
        """
        t = time.time()
        date_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(t))
        try:
            self.cursor.execute("SELECT hostid FROM hosts WHERE access_token = :t",{'t':host_token})
            host_id = self.cursor.fetchone()[0]
            self.cursor.execute("INSERT INTO meetings VALUES (:m, :h, :t, '0:00:00', :d)",{'m':meeting_token, 'h':host_id, 't':title, 'd':date_time})
            self.conn.commit()
        except sqlite3.Error as error:
            print("Error inserting into table meetings:",error)
            self.conn.rollback()

    def add_new_host(self, username, password):
        """Attempt to store new host and generates access token

        Parameters:
            username {string} -- New host username
            password {string} -- New host password

        Returns:
            None {None} -- Username already exists
            token {string} -- Token linked to host
        """
        try:
            self.cursor.execute("SELECT hostid FROM hosts WHERE username = :u",{'u':username})
            if self.cursor.fetchone() is None:
                alphabet = string.ascii_letters + string.digits
                salt = hashlib.sha256(''.join(secrets.choice(alphabet) for i in range(8)).encode('utf-8')).hexdigest()
                enc_pass = hashlib.sha256((password + "--" + salt).encode('utf-8')).hexdigest()
                while True:
                    token = hashlib.sha256(''.join(secrets.choice(alphabet) for i in range(8)).encode('utf-8')).hexdigest()
                    self.cursor.execute("SELECT hostid FROM hosts WHERE access_token = :t",{'t':token})
                    if self.cursor.fetchone() is None:
                        break
                self.cursor.execute("INSERT INTO hosts VALUES (NULL, :u, :p, :s, :t)",{'u':username, 'p':enc_pass, 's':salt, 't':token})
                self.conn.commit()
                return token
            else:
                return None
        except sqlite3.Error as error:
            print("Error encountered:",error)
            self.conn.rollback()
            return None

    def update_runtime(self, token):
        """Updates running time of meeting given by token

        Parameters:
            token {int} -- Identifier for meeting
        """
        t = time.time()
        current_time = datetime.datetime.strptime(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(t)), "%Y-%m-%d %H:%M:%S")
        try:
            self.cursor.execute("SELECT date_time FROM meetings WHERE meetingid = :m",{'m':token})
            start_time = datetime.datetime.strptime(self.cursor.fetchone()[0], "%Y-%m-%d %H:%M:%S")
            elapsed_time = current_time - start_time
            self.cursor.execute("UPDATE meetings SET runtime = :t WHERE meetingid = :m",{'t':str(elapsed_time), 'm':token})
            self.conn.commit()
        except sqlite3.Error as error:
            print(error)
            self.conn.rollback()

    def check_host(self, username, check_word):
        """Validates host's password and returns new access token

        Parameters:
            username {string} -- Host's username
            check_word {string} -- Host's password (to check)

        Returns:
            None {None} -- Credentials don't match
            token {string} -- Access token linked to host
        """
        try:
            self.cursor.execute("SELECT username FROM hosts WHERE username = :u",{'u':username})
            if self.cursor.fetchone() is None:
                return None
            else:
                self.cursor.execute("SELECT encrypted_pass, salt FROM hosts WHERE username = :u",{'u':username})
                fetched = self.cursor.fetchall()
                enc_pass = fetched[0][0]
                salt = fetched[0][1]
                check = hashlib.sha256((check_word + "--" + salt).encode('utf-8')).hexdigest()
                if check == enc_pass:
                    alphabet = string.ascii_letters + string.digits
                    while True:
                        token = hashlib.sha256(''.join(secrets.choice(alphabet) for i in range(8)).encode('utf-8')).hexdigest()
                        self.cursor.execute("SELECT hostid FROM hosts WHERE access_token = :t",{'t':token})
                        if self.cursor.fetchone() is None:
                            break
                    self.cursor.execute("UPDATE hosts SET access_token = :t WHERE username = :u",{'t':token, 'u':username})
                    self.conn.commit()
                    return token
                return None
        except sqlite3.Error as error:
            print("Error encountered",error)
            self.conn.rollback()
            return None

    def check_token(self, token):
        """Check if access token exists in DB

        Parameters:
            token {string} -- Token to check existence of

        Returns:
            True/False {boolean} -- Indicates whether token exists
        """
        try:
            self.cursor.execute("SELECT hostid FROM hosts WHERE access_token = :t",{'t':token})
            if self.cursor.fetchone() is None:
                return False
            return True
        except sqlite3.Error as error:
            print("Error encountered:",error)
            return False

    def get_meetings(self, token):
        """Return a list of all past meetings conducted by a host

        Parameters:
            token {string} -- Token linked to a host

        Returns:
            meetings {list} -- List of all meetings conducted by a host
        """
        try:
            self.cursor.execute("SELECT hostid FROM hosts WHERE access_token = :t",{'t':token})
            host_id = self.cursor.fetchone()[0]
            self.cursor.execute("SELECT title, date_time, meetingid, runtime FROM meetings WHERE hostid = :h",{'h':host_id})
            meetings = self.cursor.fetchall()
            return meetings
        except sqlite3.Error as error:
            print("Error encountered:",error)
            return []

    def get_meeting_info(self, meeting_id, host_token):
        """Return meeting information

        Parameters:
            meeting_id {int} -- Identifier for meeting
            host_token {string} -- Access token for host

        Returns:
            None {None} -- Invalid access token
            information -- Information associated with meeting ID
        """
        try:
            self.cursor.execute("SELECT access_token FROM hosts JOIN meetings ON meetings.hostid = hosts.hostid AND meetingid = :m",{'m':meeting_id})
            access_token = self.cursor.fetchone()[0]
            if host_token != access_token:
                return None
            information = {
                "mult_choice": [],          # [[poll, [answers], [frequency]]]
                "question": [],             # [[question, [responses]]]
                "final_mood": 0,            # Final mood value
                "average_mood": 0,          # Overall average mood
                "emoji": [],                # [emoji frequencies]
                "errors": [],               # [errors]
                "general_feedback": []      # [feedback]
            }

            self.cursor.execute(""" SELECT questionasked, attendeeanswer
                                    FROM mult_choice_responses
                                    JOIN responses USING (responseid)
                                    JOIN feedback ON
                                        responses.feedbackid = feedback.feedbackid AND
                                        meetingid = :m""",{'m':meeting_id})
            polls = self.cursor.fetchall()
            if polls is not None:
                questions = {}
                for poll in polls:
                    question = poll[0]
                    choice = poll[1]
                    if question not in questions:
                        questions[question] = {}
                    if choice not in questions[question]:
                        questions[question][choice] = 0
                    questions[question][choice] += 1
                multiple_choices = []
                for question in questions:
                    choices = []
                    frequencies = []
                    for choice in questions[question]:
                        choices.append(choice)
                        frequencies.append(questions[question][choice])
                    multiple_choices.append([question, choices, frequencies])
                information["mult_choice"] = multiple_choices

            self.cursor.execute(""" SELECT questionasked, txtmessage
                                    FROM text_responses
                                    JOIN responses USING (responseid)
                                    JOIN feedback ON
                                        responses.feedbackid = feedback.feedbackid AND
                                        meetingid = :m""",{'m':meeting_id})
            responses = self.cursor.fetchall()
            if responses is not None:
                texts = {}
                for response in responses:
                    asked = response[0]
                    answer = response[1]
                    if asked not in texts:
                        texts[asked] = []
                    texts[asked].append(answer)
                question = []
                for text in texts:
                    answers = texts[text]
                    question.append([text,answers])
                information["question"] = question

            self.cursor.execute(""" SELECT errmessage 
                                    FROM errors 
                                    JOIN feedback ON 
                                        errors.feedbackid = feedback.feedbackid AND 
                                        meetingid = :m""",{'m':meeting_id})
            err_messages = self.cursor.fetchall()
            if err_messages is not None:
                for message in err_messages:
                    information["errors"].append(message[0])

            self.cursor.execute(""" SELECT score, avgmood, txtmessage
                                    FROM text_moods
                                    JOIN moods USING (moodid)
                                    JOIN feedback ON
                                        moods.feedbackid = feedback.feedbackid AND
                                        meetingid = :m
                                    ORDER BY timeofmood ASC""",{'m':meeting_id})
            text_moods = self.cursor.fetchall()
            if text_moods is not None:
                information["final_mood"] = text_moods[-1][0]
                information["average_mood"] = text_moods[-1][1]
                for mood in text_moods:
                    information["general_feedback"].append(mood[0]) # feedback score
                    # information["general_feedback"].append(mood[2]) # feedback message
                    # information["general_feedback"].append([mood[0],mood[2]]) # feedback score and message

            self.cursor.execute(""" SELECT score
                                    FROM emoji_moods
                                    JOIN moods USING (moodid)
                                    JOIN feedback ON
                                        moods.feedbackid = feedback.feedbackid AND
                                        meetingid = :m""",{'m':meeting_id})
            scores = self.cursor.fetchall()
            if scores is not None:
                emoji = [0,0,0,0,0]
                for score in scores:
                    emoji[int(2*(score[0]+1))] += 1
                information["emoji"] = emoji

            return information
        except sqlite3.Error as error:
            print("Error encountered:",error)
            return None

    # Searches for all meetings with a certain string in their title
    def search_meetings(self,query):
        query = "%" + query + "%"
        try:
            self.cursor.execute("SELECT title, date_time, meetingid FROM meetings WHERE title LIKE ?",(query,))
            matches = self.cursor.fetchall()
            return matches

        except sqlite3.Error as error:
            return error
    
    def mult_choice_frequency(self,question):
        try:
            self.cursor.execute("SELECT attendeeanswer, COUNT(attendeeanswer) FROM mult_choice_responses INNER JOIN responses ON mult_choice_responses.responseid = responses.responseid WHERE responses.questionasked = ? GROUP BY attendeeanswer",(question,))
            results = self.cursor.fetchall()
            return results
        
        except sqlite3.Error as error:
            return error
    
    def sentiment_history(self, mood_type, meeting):
        try:
            self.cursor.execute("SELECT timeofmood, avgmood FROM moods INNER JOIN feedback ON moods.feedbackid = feedback.feedbackid WHERE moodtype = ? AND meetingid = ?",(mood_type,meeting,))
            results = self.cursor.fetchall()
            return results
        except sqlite3.Error as error:
            return error
