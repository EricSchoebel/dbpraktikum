DROP TABLE IF EXISTS Friendship;
DROP TABLE IF EXISTS User;

CREATE TABLE User (
  uid     SERIAL PRIMARY KEY,
  name    VARCHAR(100)
);

CREATE TABLE Friendship (
  uid1    INT,
  uid2    INT,
  Fgrad   VARCHAR(100),
  PRIMARY KEY (uid1, uid2),
  FOREIGN KEY (uid1) REFERENCES Nutzer (uid),
  FOREIGN KEY (uid2) REFERENCES Nutzer (uid)
);


INSERT INTO User(name) VALUES
  ('Diana'),
  ('Johann'),
  ('Kathleen'),
  ('Ralf'),
  ('Isabell'),
  ('Dennis');

INSERT INTO Friendship(uid1, uid2, fGrad) VALUES
  (1, 2, 'lego buddy'),
  (3, 4, 'climbing buddy'),
  (1, 5, 'office buddy'),
  (2, 5, 'party buddy'),
  (3, 6, 'lunch buddy'),
  (4, 6, 'lunch buddy'),
  (1, 6, 'lunch buddy'),
  (2, 4, 'basketball buddy');