-- Tạo bảng "User"
CREATE TABLE "User" (
    student_id INT UNIQUE NOT NULL,
    user_id SERIAL PRIMARY KEY,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Tạo bảng Subject
CREATE TABLE Subject (
    subject_id VARCHAR(6) PRIMARY KEY,
    name_subject VARCHAR(255) NOT NULL,
    credits INT CHECK (credits > 0)
);

-- Tạo bảng Class
CREATE TABLE Class (
    class_id VARCHAR(4) PRIMARY KEY,
    subject_id VARCHAR(6) NOT NULL,
    current_slots INT DEFAULT 0 CHECK (current_slots >= 0),
    max_slots INT CHECK (max_slots > 0),
    lecturer VARCHAR(255),
    schedule TEXT,
    FOREIGN KEY (subject_id) REFERENCES Subject(subject_id)
);

-- Tạo bảng Regis với thêm trường subject_id
CREATE TABLE Regis (
    id SERIAL PRIMARY KEY,
    student_id INT NOT NULL,
    class_id VARCHAR(4) NOT NULL,
    subject_id VARCHAR(6) NOT NULL,
    date TIMESTAMP DEFAULT NOW(),
    FOREIGN KEY (student_id) REFERENCES "User"(student_id),
    FOREIGN KEY (class_id) REFERENCES Class(class_id),
    FOREIGN KEY (subject_id) REFERENCES Subject(subject_id),
    UNIQUE(student_id, class_id)  -- Đảm bảo một sinh viên chỉ đăng ký một lớp học một lần
);

-- Thêm data mẫu vào bảng "User"
INSERT INTO "User" (student_id, created_at) VALUES
(21110108, NOW()),
(21110109, NOW()),
(21110110, NOW());

-- Thêm data mẫu vào bảng Subject
INSERT INTO Subject (subject_id, name_subject, credits) VALUES
('IT1001', 'Lập trình Java', 3),
('IT1002', 'Cơ sở dữ liệu', 4),
('MA1001', 'Giải tích 1', 3);

-- Thêm data mẫu vào bảng Class
INSERT INTO Class (class_id, subject_id, max_slots, lecturer, schedule) VALUES
('IT01', 'IT1001', 50, 'Nguyễn Văn A', 'Thứ 2, 7h30 - 9h30'),
('IT02', 'IT1001', 45, 'Trần Thị B', 'Thứ 4, 13h30 - 15h30'),
('DB01', 'IT1002', 60, 'Lê Văn C', 'Thứ 5, 9h30 - 11h30');

-- Thêm data mẫu vào bảng Regis
INSERT INTO Regis (student_id, class_id, subject_id, date) VALUES
(21110108, 'IT01', 'IT1001', NOW()),
(21110109, 'IT01', 'IT1001', NOW()),
(21110110, 'DB01', 'IT1002', NOW());

-- Kiểm tra dữ liệu bảng Class
SELECT class_id, subject_id, current_slots, max_slots, lecturer, schedule FROM Class;

-- Kiểm tra dữ liệu bảng "User"
SELECT * FROM "User";

-- Kiểm tra dữ liệu bảng Subject
SELECT * FROM Subject;

-- Kiểm tra dữ liệu bảng Regis
SELECT * FROM Regis;
