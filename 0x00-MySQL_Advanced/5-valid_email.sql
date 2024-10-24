-- 5-valid_email
-- creates a trigger that resets the attribute valid_email only when the email has changed
DELIMITER $$
CREATE TRIGGER valid_email_AUPD
BEFORE UPDATE ON users
FOR EACH ROW
BEGIN
IF OLD.email <> NEW.email THEN
SET NEW.valid_email = 0;
END IF;
END $$
