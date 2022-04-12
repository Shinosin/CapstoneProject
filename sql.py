CREATE_STUDENT = '''
CREATE TABLE IF NOT EXISTS student(
    student_id INTEGER,
    student_name TEXT,
    student_age INTEGER,
    year_enrolled INTEGER,
    graduating_year INTEGER,
    student_class INTEGER
    PRIMARY KEY(student_id),
    FOREIGN KEY(student_class) REFERENCES class(class_id)
);
'''

CREATE_CLASS = '''
CREATE TABLE IF NOT EXISTS class(
    class_id INTEGER,
    class_name TEXT,
    class_level TEXT CHECK(
        class_level IN ("JC1", "JC2")
        ),
    PRIMARY KEY (class_id)
);
'''

CREATE_SUBJECT = '''
CREATE TABLE IF NOT EXISTS subject(
    subject_id INTEGER,
    subject_name TEXT CHECK('GP', 'MATH', 'FM', 'COMP', 'PHY', 'CHEM', 'ECONS', 'BIO', 'GEO', 'HIST', 'ELIT', 'ART', 'CLTRANS', 'CL', 'ML', 'TL', 'CLL', 'CLB', 'PW', 'PUNJABI', 'HINDI', 'BENGALESE', 'JAPANESE'
        ),
    subject_level TEXT CHECK(
        subject_level IN ("H1", "H2", "H3")
        ),
    PRIMARY KEY (subject_code)
);
'''

CREATE_CCA = '''
CREATE TABLE IF NOT EXISTS cca(
    cca_id INTEGER,
    cca_name TEXT,
    PRIMARY KEY(cca_id)
);
'''

CREATE_ACTIVITY = '''
CREATE TABLE IF NOT EXISTS activity(
    activity_id INTEGER,
    start_date TEXT,
    end_date TEXT,
    description TEXT,
    PRIMARY KEY(activity_id)
);
'''

CREATE_STUDENT_SUBJECT = '''
CREATE TABLE IF NOT EXISTS student_subject(
    student_id INTEGER,
    subject_id INTEGER,
    PRIMARY KEY (student_id),
    PRIMARY KEY (subject_id),
    FOREIGN KEY (student_id) REFERENCES student(student_id),
    FOREIGN KEY (subject_id) REFERENCES subject(subject_id)
);
'''

CREATE_STUDENT_CCA = '''
CREATE TABLE IF NOT EXISTS student_cca(
    student_id INTEGER,
    cca_id INTEGER,
    role TEXT,
    PRIMARY KEY (student_id),
    PRIMARY KEY (cca_id),
    FOREIGN KEY (student_id) REFERENCES student(student_id),
    FOREIGN KEY (cca_id) REFERENCES cca(cca_id)
);
'''

CREATE_STUDENT_ACTIVITY = '''
CREATE TABLE IF NOT EXISTS student_activity(
    student_id INTEGER
    activity_id INTEGER
    category TEXT CHECK('Achievement', 'Enrichment', 'Leadership', 'Service'
    ),
    role TEXT
    award TEXT
    hours INTEGER
    PRIMARY KEY (student_id),
    PRIMARY KEY (activity_id),
    FOREIGN KEY (student_id) REFERENCES student(student_id),
    FOREIGN KEY (activity_id) REFERENCES activity(activity_id)
);
'''