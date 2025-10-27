use chatbotdb

START TRANSACTION;

INSERT INTO auth_user
  (password, last_login, is_superuser, username, first_name, last_name,
   email, is_staff, is_active, date_joined)
VALUES
  ('pbkdf2_sha256$260000$fQkAIBuQqEBRTTdg$j0esXQi+1+qtJSFJF/SoiGUP2ZgSu8USbMldTftOo+g=',
   NULL, 0,
   'test', '', '',
   'test@example.com', 0, 1, NOW(6));
