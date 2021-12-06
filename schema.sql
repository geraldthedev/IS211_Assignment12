CREATE TABLE students (
    id INT PRIMARY KEY AUTOINCREMENT,
    name TEXT,
);

CREATE TABLE quizzes (
    id INT PRIMARY KEY AUTOINCREMENT,
    subject TEXT,
    quiz_questions INT,
    date DATE,
);

CREATE TABLE student_quiz_results(
    id INT PRIMARY KEY AUTOINCREMENT,
    student TEXT,
    FOREIGN KEY(student) REFERENCES students(first_name, last_name),
    score INT,
);
