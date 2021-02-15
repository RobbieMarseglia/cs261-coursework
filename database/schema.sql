DROP TABLE IF EXISTS hosts;
CREATE TABLE hosts (
    hostid  INTEGER,
    PRIMARY KEY (hostid)
);

DROP TABLE IF EXISTS meetings;
CREATE TABLE meetings (
    meetingid  INTEGER,
    title      VARCHAR(30) NOT NULL,
    runtime    TIME NOT NULL,
    PRIMARY KEY (meetingid)
);

DROP TABLE IF EXISTS feedback;
CREATE TABLE feedback (
    feedbackid    INTEGER,
    meetingid     INTEGER,
    userid        INTEGER NOT NULL,
    feedbacktype  VARCHAR(8) NOT NULL CHECK (feedbacktype IN ('Error','Question','Response','Mood')),
    PRIMARY KEY (feedbackid),
    FOREIGN KEY (meetingid) REFERENCES meetings(meetingid)
);

DROP TABLE IF EXISTS errors;
CREATE TABLE errors (
    feedbackid  INTEGER,
    errortype   VARCHAR(10) NOT NULL,
    errmessage  VARCHAR(50) NOT NULL,
    PRIMARY KEY (feedbackid),
    FOREIGN KEY (feedbackid) REFERENCES feedback(feedbackid)
);

DROP TABLE IF EXISTS questions;
CREATE TABLE questions (
    feedbackid  INTEGER,
    qmessage    VARCHAR(50) NOT NULL,
    PRIMARY KEY (feedbackid),
    FOREIGN KEY (feedbackid) REFERENCES feedback(feedbackid)
);

DROP TABLE IF EXISTS moods;
CREATE TABLE moods (
    moodid      INTEGER,
    feedbackid  INTEGER,
    moodtype    VARCHAR(5) NOT NULL CHECK (moodtype IN ('Text','Emoji')),
    score       FLOAT NOT NULL,
    timeofmood  TIME NOT NULL,
    PRIMARY KEY (moodid),
    FOREIGN KEY (feedbackid) REFERENCES feedback(feedbackid)
);

DROP TABLE IF EXISTS text_moods;
CREATE TABLE text_moods (
    moodid      INTEGER,
    txtmessage  VARCHAR(50) NOT NULL,
    PRIMARY KEY (moodid),
    FOREIGN KEY (moodid) REFERENCES moods(moodid)
);

DROP TABLE IF EXISTS emoji_moods;
CREATE TABLE emoji_moods (
    moodid     INTEGER,
    emojitype  VARCHAR(10) NOT NULL,
    PRIMARY KEY (moodid),
    FOREIGN KEY (moodid) REFERENCES moods(moodid)
);

DROP TABLE IF EXISTS responses;
CREATE TABLE responses (
    responseid     INTEGER,
    feedbackid     INTEGER,
    responsetype   VARCHAR(10) NOT NULL CHECK (responsetype IN ('Text','Emoji','MultChoice')),
    questionasked  VARCHAR(50) NOT NULL,
    PRIMARY KEY (responseid),
    FOREIGN KEY (feedbackid) REFERENCES feedback(feedbackid)
);

DROP TABLE IF EXISTS text_responses;
CREATE TABLE text_responses (
    responseid  INTEGER,
    txtmessage  VARCHAR(50) NOT NULL,
    PRIMARY KEY (responseid),
    FOREIGN KEY (responseid) REFERENCES responses(responseid)
);

DROP TABLE IF EXISTS emoji_responses;
CREATE TABLE emoji_responses (
    responseid  INTEGER,
    emojitype   VARCHAR(10) NOT NULL,
    PRIMARY KEY (responseid),
    FOREIGN KEY (responseid) REFERENCES responses(responseid)
);

DROP TABLE IF EXISTS mult_choice_responses;
CREATE TABLE mult_choice_responses (
    responseid     INTEGER,
    correctanswer  VARCHAR(10) NOT NULL,
    useranswer     VARCHAR(10) NOT NULL,
    PRIMARY KEY (responseid),
    FOREIGN KEY (responseid) REFERENCES responses(responseid)
);