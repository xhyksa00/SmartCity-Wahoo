DROP TABLE IF EXISTS login_info;
DROP TABLE IF EXISTS admin_info;
DROP TABLE IF EXISTS image;
DROP TABLE IF EXISTS service_request_comments;
DROP TABLE IF EXISTS ticket_comments;
DROP TABLE IF EXISTS service_request;
DROP TABLE IF EXISTS ticket;
DROP TABLE IF EXISTS user;

DROP TRIGGER IF EXISTS set_ticket_in_progress;
DROP TRIGGER IF EXISTS set_request_technician_null;

CREATE TABLE user (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(20) NOT NULL,
    surname VARCHAR(20) NOT NULL,
    role ENUM ('Citizen','Officer','Technician') DEFAULT 'Citizen'
);

CREATE TABLE login_info(
    email VARCHAR(50) PRIMARY KEY NOT NULL,
    userId INT,
    FOREIGN KEY (userId)
        REFERENCES user(id)
        ON DELETE CASCADE,
    password VARCHAR(60) NOT NULL
);

CREATE TABLE admin_info(
    username VARCHAR(5) PRIMARY KEY NOT NULL DEFAULT 'admin',
    password VARCHAR(60) NOT NULL
);

CREATE TABLE ticket (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(50) NOT NULL,
    description TEXT(1000) NOT NULL,
    state ENUM ('Open','Waiting For Approval','In Progress','Closed: Fixed','Closed: Denied','Closed: Duplicate'),
    created_timestamp TIMESTAMP DEFAULT current_timestamp,
    priority ENUM ('Lowest','Low','Medium','High','Highest') NOT NULL,
    authorId INT,
    FOREIGN KEY (authorId) REFERENCES user(id) ON DELETE SET NULL
);

CREATE TABLE service_request (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    description TEXT(1000) NOT NULL,
    created_timestamp TIMESTAMP DEFAULT current_timestamp,
    days_remaining INT DEFAULT 0,
    price INT DEFAULT 0,
    priority ENUM ('Lowest','Low','Medium','High','Highest') NOT NULL,
    state ENUM ('Open', 'In Progress', 'Finished'),
    ticketId INT,
    FOREIGN KEY (ticketId) REFERENCES ticket(id) ON DELETE CASCADE,
    technicianId INT,
    FOREIGN KEY (technicianId) REFERENCES user(id) ON DELETE SET NULL,
    authorId INT,
    FOREIGN KEY (authorId) REFERENCES user(id) ON DELETE SET NULL
);

CREATE TABLE ticket_comments (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    text VARCHAR(255),
    created_timestamp TIMESTAMP DEFAULT current_timestamp,
    ticketId INT,
    FOREIGN KEY (ticketId) REFERENCES ticket(id) ON DELETE CASCADE,
    authorId INT,
    FOREIGN KEY (authorId) REFERENCES user(id) ON DELETE SET NULL
);

CREATE TABLE service_request_comments (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    text VARCHAR(255),
    created_timestamp TIMESTAMP DEFAULT current_timestamp,
    authorId INT,
    FOREIGN KEY (authorId) REFERENCES user(id) ON DELETE SET NULL,
    requestId INT,
    FOREIGN KEY (requestId) REFERENCES service_request(id) ON DELETE CASCADE
);

CREATE TABLE image (
#     name VARCHAR(50) PRIMARY KEY,
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    url VARCHAR(255) NOT NULL,
    ticketId INT,
    FOREIGN KEY (ticketId) REFERENCES ticket(id) ON DELETE CASCADE
);

-- TRIGGERS

-- sets Ticket state to 'In Progress' after
-- a service request that references it is created
CREATE TRIGGER set_ticket_in_progress
    AFTER INSERT ON service_request
    FOR EACH ROW
    begin
        DECLARE ticket_exists BOOLEAN;
        SELECT 1 INTO ticket_exists
        FROM ticket WHERE ticket.id = NEW.ticketId;

        if ticket_exists = 1 then
            UPDATE ticket
            SET state = 'In Progress'
            WHERE id = NEW.ticketId;
        end if;
    end;

CREATE TRIGGER set_request_technician_null
    BEFORE UPDATE ON user
    FOR EACH ROW
    BEGIN
        DECLARE user_role VARCHAR(11);
        SELECT role INTO user_role
        FROM user WHERE user.id = NEW.id;

        IF user_role = 'technician' THEN
            UPDATE service_request
            SET technicianId = NULL
            WHERE technicianId = NEW.id;
        END IF;
    END;

-- INSERT SAMPLE DATA

-- ADMIN
INSERT INTO admin_info (username, password)
VALUES ('admin', '$2b$12$3Jjxd9gbeno3xFiGNzVaneqgStxPXTE551.aDNFWUTdagj4ukprve');

-- USERS
INSERT INTO user (name, surname, role)
VALUES
    ('Jan', 'Novak', 'citizen'),
    ('Don Leopold', 'Juan Nemcek', 'citizen'),
    ('Samko', 'Sadik', 'citizen'),
    ('Tech', 'Nician', 'technician'),
    ('Of', 'Ficer', 'officer');

INSERT INTO login_info (email, userId, password)
VALUES
    ('jan.novak@gmail.com', 1, '$2b$12$DNLUpKOzdfSWxx232ng3eee70n47lAZHvMGrq1Bwry2ZO/PPlekNS'),
    ('don.juan@gmail.com', 2, '$2b$12$obxW/cGVbfI2WLP1rKJAVOhLHU3QkuxC58kJ5ZvwCd0pDJ8ROrbqS'),
    ('s@s.s', 3, '$2b$12$cb/OKBCpExqNPAw8BRTCyOU/F7MKJlqh9MbwHRVBMinowCg1UaihK'),
    ('tech@nician.com', 4, '$2b$12$A4PTGg5TFm1YecVbhgqviODRfu1SMOqnXQbk548kydUk6xBNaBzh.'),
    ('of@ficer.com', 5, '$2b$12$s2hc9RGBLNj7SpasSGiZoOnW8zUkaLdfJRU0sr5K9xJk2NX1U32eS');

-- TICKETS
INSERT INTO ticket (title, description, state, priority, authorId)
VALUES
    (   'Faulty street lamp',
        'The street lamp on the corner of Sample Street and Made-up Ave. blinks rapidly for about 10 seconds every 5 or so minutes.',
        'Open', 'Lowest', 1),
    (   'Leaking hydrant',
        'The hydrant on the corner of Sample Street and Made-up Ave. is leaking water slowly.',
        'Open', 'Medium', 2);
