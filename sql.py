#sql statements for storage.py

## sql create statements ##

CREATE_STUDENT = '''
CREATE TABLE IF NOT EXISTS student(
    id INTEGER,
    name TEXT,
    age INTEGER,
    year_enrolled INTEGER,
    graduating_year INTEGER,
    student_class INTEGER
    PRIMARY KEY(id),
    FOREIGN KEY(student_class) REFERENCES class(id)
);
'''

CREATE_CLASS = '''
CREATE TABLE IF NOT EXISTS class(
    id INTEGER,
    name TEXT,
    level TEXT CHECK(
        level IN ("JC1", "JC2")
        ),
    PRIMARY KEY (id)
);
'''

CREATE_SUBJECT = '''
CREATE TABLE IF NOT EXISTS subject(
    subject_code TEXT,
    name TEXT CHECK(
        name IN ('PG', 'MATH', 'FM', 'COMP', 'PHY', 'CHEM', 'ECONS', 'BIO', 'GEO', 'HIST', 'ELIT', 'ART', 'CLTRANS', 'CL', 'ML', 'TL', 'CLL', 'CLB', 'PW', 'PUNJABI', 'HINDI', 'BENGALESE', 'JAPANESE')
        ),
    level TEXT CHECK(
        level IN ("H1", "H2", "H3")
        ),
    PRIMARY KEY (subject_code)
);
'''

CREATE_CCA = '''
CREATE TABLE IF NOT EXISTS cca(
    id INTEGER,
    name TEXT,
    PRIMARY KEY(id)
);
'''

CREATE_ACTIVITY = '''
CREATE TABLE IF NOT EXISTS activity(
    id INTEGER,
    name TEXT,
    start_date TEXT,
    end_date TEXT,
    description TEXT,
    PRIMARY KEY(id)
);
'''

CREATE_STUDENT_SUBJECT = '''
CREATE TABLE IF NOT EXISTS student_subject(
    student_id INTEGER,
    subject_code INTEGER,
    PRIMARY KEY (student_id),
    PRIMARY KEY (subject_id),
    FOREIGN KEY (student_id) REFERENCES student(id),
    FOREIGN KEY (subject_code) REFERENCES subject(subject_code)
);
'''

CREATE_STUDENT_CCA = '''
CREATE TABLE IF NOT EXISTS student_cca(
    student_id INTEGER,
    cca_id INTEGER,
    role TEXT,
    PRIMARY KEY (student_id),
    PRIMARY KEY (cca_id),
    FOREIGN KEY (student_id) REFERENCES student(id),
    FOREIGN KEY (cca_id) REFERENCES cca(id)
);
'''

CREATE_STUDENT_ACTIVITY = '''
CREATE TABLE IF NOT EXISTS student_activity(
    student_id INTEGER
    activity_id INTEGER
    category TEXT CHECK('ACHIEVEMENT', 'ENRICHMENT', 'LEADERSHIP', 'SERVICE'
    ),
    role TEXT DEFAULT 'PARTICIPANT'
    award TEXT
    hours INTEGER
    PRIMARY KEY (student_id),
    PRIMARY KEY (activity_id),
    FOREIGN KEY (student_id) REFERENCES student(id),
    FOREIGN KEY (activity_id) REFERENCES activity(id)
);
'''

## sql insert statements ##
INSERT_STUDENT = '''
    INSERT INTO student(
        name, age, year_enrolled, graduating_year, student_class
    ) 
    VALUES(
        :name, :age, :year_enrolled, :graduating_year, :student_class
    );
'''

INSERT_CLASS = '''
    INSERT INTO class(
        name, level
    )
    VALUES(
        :name, :level
    );
'''

INSERT_SUBJECT = '''
    INSERT INTO subject(
       subject_code, name, level 
    )
    VALUES(
        :subject_code, :name, :level
    );
'''

INSERT_CCA = '''
    INSERT INTO cca(
        name
    )
    VALUES(
        :name
    );
'''

INSERT_ACTIVITY = '''
    INSERT INTO activity(
        name, start_date, end_date, description
    )
    VALUES(
        :name, :start_date, :end_date, :description
    );
'''

INSERT_STUDENT_SUBJECT = '''
    INSERT INTO student_subject(
        student_id, subject_code
    )
    VALUES(
        :student_id, :subject_code
    );
'''

INSERT_STUDENT_CCA = '''
    INSERT INTO student_cca(
        student_id, cca_id, role
    )
    VALUES(
        :student_id, :cca_id, :role
    );
'''

INSERT_STUDENT_ACTIVITY = '''
    INSERT INTO student_activity(
        student_id, activity_id, category, role, award, hours
    )
    VALUES(
        :student_id, :activity_id, :category, :role, :award, :hours
    );
'''