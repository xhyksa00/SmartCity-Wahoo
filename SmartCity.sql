DROP TABLE IF EXISTS login_info;
DROP TABLE IF EXISTS images;
DROP TABLE IF EXISTS service_request_comments;
DROP TABLE IF EXISTS ticket_comments;
DROP TABLE IF EXISTS service_request;
DROP TABLE IF EXISTS ticket;
DROP TABLE IF EXISTS user;

CREATE TABLE user (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(20) NOT NULL,
    surname VARCHAR(20) NOT NULL,
    role  VARCHAR(10) CHECK( role IN ('citizen','officer','technician','admin'))
);

CREATE TABLE login_info(
    user_id INT,
    FOREIGN KEY (user_id)
        REFERENCES user(id)
        ON DELETE CASCADE,
    email VARCHAR(50) NOT NULL,
    password VARCHAR(100) NOT NULL
);

CREATE TABLE ticket (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(50) NOT NULL,
    description VARCHAR(255) NOT NULL,
    state  VARCHAR(13) CHECK(
        state IN ('open','waiting','inProgress','cls-denied','cls-fixed','cls-duplicate')),
    created_timestamp TIMESTAMP DEFAULT current_timestamp,
    priority  VARCHAR(7) CHECK( priority IN ('lowest','low','regular','high','highest')),
    author INT,
    FOREIGN KEY (author) REFERENCES user(id) ON DELETE SET NULL,
    service_request INT REFERENCES service_request(id)
);

CREATE TABLE service_request (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    description VARCHAR(255) NOT NULL,
    created_timestamp TIMESTAMP DEFAULT current_timestamp,
    days_remaining INT DEFAULT 0,
    price INT DEFAULT 0,
    priority VARCHAR(7) CHECK( PRIORITY IN ('lowest','low','regular','high','highest')),
    state VARCHAR(10) CHECK( state IN ('open','inProgress','done')),
    technician INT,
    FOREIGN KEY (technician) REFERENCES user(id) ON DELETE SET NULL,
    author INT,
    FOREIGN KEY (author) REFERENCES user(id) ON DELETE SET NULL
);

CREATE TABLE ticket_comments (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    text VARCHAR(255),
    created_timestamp TIMESTAMP DEFAULT current_timestamp,
    ticket INT,
    FOREIGN KEY (ticket) REFERENCES ticket(id) ON DELETE CASCADE,
    author INT,
    FOREIGN KEY (author) REFERENCES user(id) ON DELETE SET NULL
);

CREATE TABLE service_request_comments (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    text VARCHAR(255),
    created_timestamp TIMESTAMP DEFAULT current_timestamp,
    ticket_id INT,
    FOREIGN KEY (ticket_id) REFERENCES  ticket (id) ON DELETE SET NULL,
    author INT,
    FOREIGN KEY (author) REFERENCES user(id) ON DELETE SET NULL,
    request INT,
    FOREIGN KEY (request) REFERENCES service_request(id) ON DELETE CASCADE
);

CREATE TABLE images (
    name VARCHAR(50) PRIMARY KEY,
    ticket_id INT,
    FOREIGN KEY (ticket_id) REFERENCES ticket (id) ON DELETE CASCADE
);

-- triggers
DROP TRIGGER IF EXISTS service_request_technician;
CREATE TRIGGER service_request_technician
 BEFORE
 INSERT
 ON service_request
 FOR EACH ROW
 BEGIN
    DECLARE role VARCHAR(10);
     SELECT c.role
         INTO role
         FROM user c
         WHERE c.id = new.technician;
     IF role != 'technician' THEN
         SIGNAL SQLSTATE '45000' SET message_text = 'Assigned user is not a technician.';
     END IF;
 END;

DROP TRIGGER IF EXISTS service_request_author;
CREATE TRIGGER service_request_author
 BEFORE
 INSERT
 ON service_request
 FOR EACH ROW
 BEGIN
     DECLARE role VARCHAR(10);
     SELECT c.role
         INTO role
         FROM user c
         WHERE c.id = new.author;
     IF role != 'officer' THEN
         SIGNAL SQLSTATE '45000' SET message_text = 'Only officers can create service requests.';
     END IF;
 END;

-- INSERT SAMPLE DATA
INSERT INTO user (name, surname, role)
VALUES ('Jan', 'Novak', 'citizen');
INSERT INTO login_info(email, password)
VALUES ('jan.novak@gmail.com', 'tmpPwd');

INSERT INTO user (name, surname, role)
VALUES ('Don Leopold', 'Juan Nemcek', 'technician');
INSERT INTO login_info(email, password)
VALUES ('don.juan@gmail.com', 'terribleBurger86');

INSERT INTO ticket (title, description, state, author)
VALUES ('Faulty street lamp', 'The street lamp on the corner of Sample Street and Made-up Ave. blinks rapidly for about 10 seconds every 5 or so minutes.',
        'open', (SELECT id FROM user WHERE surname = 'Novak'));
INSERT INTO ticket (title, description, state, author)
VALUES ('Leaking hydrant', 'The hydrant on the corner of Sample Street and Made-up Ave. is leaking water slowly.',
        'open', (SELECT id FROM user WHERE surname = 'Juan Nemcek'));