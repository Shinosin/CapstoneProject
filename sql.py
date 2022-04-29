#sql statements for storage.py

## sql create statements ##

CREATE_STUDENT = '''
CREATE TABLE IF NOT EXISTS student (
    id INTEGER,
    name TEXT,
    age INTEGER,
    year_enrolled INTEGER,
    graduating_year INTEGER,
    student_class INTEGER,
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
    name TEXT CHECK (
        name IN ('GP', 'MATH', 'FM', 'COMP', 'PHY', 'CHEM', 'ECONS', 'BIO', 'GEO', 'HIST', 'ELIT', 'ART', 'CLTRANS', 'CL', 'ML', 'TL', 'CLL', 'CLB', 'PW', 'PUNJABI', 'HINDI', 'BENGALESE', 'JAPANESE')
        ),
    level TEXT CHECK(
        level IN ("H1", "H2", "H3")
        ),
    PRIMARY KEY (subject_code)
);
'''

CREATE_CCA = '''
CREATE TABLE IF NOT EXISTS cca (
    id INTEGER,
    name TEXT,
    PRIMARY KEY(id)
);
'''

CREATE_ACTIVITY = '''
CREATE TABLE IF NOT EXISTS activity (
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
    PRIMARY KEY (student_id, subject_code),
    FOREIGN KEY (student_id) REFERENCES student(id),
    FOREIGN KEY (subject_code) REFERENCES subject(subject_code)
);
'''

CREATE_STUDENT_CCA = '''
CREATE TABLE IF NOT EXISTS student_cca(
    student_id INTEGER,
    cca_id INTEGER,
    role TEXT DEFAULT 'MEMBER',
    PRIMARY KEY (student_id, cca_id),
    FOREIGN KEY (student_id) REFERENCES student(id),
    FOREIGN KEY (cca_id) REFERENCES cca(id)
);
'''

CREATE_STUDENT_ACTIVITY = '''
CREATE TABLE IF NOT EXISTS student_activity(
    student_id INTEGER,
    activity_id INTEGER,
    category TEXT CHECK (
        category IN ('ACHIEVEMENT', 'ENRICHMENT', 'LEADERSHIP', 'SERVICE')
    ),
    role TEXT DEFAULT 'PARTICIPANT',
    award TEXT,
    hours INTEGER,
    coordinator INT,
    PRIMARY KEY (student_id, activity_id),
    FOREIGN KEY (student_id) REFERENCES student(id),
    FOREIGN KEY (activity_id) REFERENCES activity(id),
    FOREIGN KEY (coordinator) REFERENCES cca(id)
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

IN_CCA = '''
    SELECT student.id, student.name, class.name AS class
    FROM student, class, student_cca
    WHERE student_cca.cca_id = ? AND
    student_cca.student_id = student.id AND
    student.student_class = "class".id;
'''

NOT_IN_CCA = '''
    SELECT student.id, student.name, class.name AS class
    FROM student
    LEFT JOIN student_cca
    ON student.id = student_cca.student_id
    LEFT JOIN class
    ON student.student_class = class.id
    WHERE student.id IN (
        SELECT id
        FROM student
        WHERE id NOT IN (
            SELECT student_id
            FROM student_cca
            WHERE cca_id = ?
        )
    )
'''
    # it wont work cuz some students dont have a cca like its null so it wont appear
    # SELECT student.id, student.name, class.name AS class
    # FROM student, class, student_cca

    # WHERE student_cca.cca_id != ? AND
    # student_cca.student_id = student.id AND
    # student.student_class = class.id;

DELETE_STUDENT_CCA = '''
    DELETE FROM student_cca
    WHERE student_id = ? AND
    cca_id = ?;
'''

UPDATE_STUDENT_CCA = '''
    UPDATE student_cca
    SET role = ?
    WHERE student_id = ? NAD
    cca_id = ?;
'''
SELECT_BY_STUDENT_ID = '''
    SELECT student.id, student.name, class.name AS class
    FROM student
    JOIN class
    ON student.student_class = class.id
    WHERE student.id = ?;
'''

DELETE_STUDENT_ACTIVITY = '''
    DELETE FROM student_activity
    WHERE student_id = ? AND
    activity_id = ?;
'''

DISPLAY_MEMBERSHIP = '''
    SELECT student.name, class.name AS class, student_cca.role
    FROM student, class, student_cca
    WHERE student_cca.cca_id = ? AND
    student_cca.student_id = student.id AND
    student.student_class = "class".id;
'''

IN_ACTIVITY = '''
    SELECT student.id, student.name, class.name AS class
    FROM student, class, student_activity
    WHERE student_activity.activity_id = ? AND
    student_activity.student_id = student.id AND
    student.student_class = "class".id;
'''

NOT_IN_ACTIVITY = '''
    SELECT student.id, student.name, class.name AS class
    FROM student
    LEFT JOIN student_activity
    ON student.id = student_activity.student_id
    LEFT JOIN class
    ON student.student_class = class.id
    WHERE student.id IN (
        SELECT id
        FROM student
        WHERE id NOT IN (
            SELECT student_id
            FROM student_activity
            WHERE activity_id = ?;
        )
    )
'''