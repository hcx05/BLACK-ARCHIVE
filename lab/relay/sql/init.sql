-- LEDGER internal database (case index + service credentials)

CREATE DATABASE IF NOT EXISTS ledger;
USE ledger;

-- Broader dependent case index (background data, not the primary IDOR target)
CREATE TABLE dependent_case_index (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    colony VARCHAR(100),
    dob VARCHAR(20),
    status VARCHAR(100),
    case_ref VARCHAR(30),
    guardian_contact VARCHAR(100)
);

INSERT INTO dependent_case_index (name, colony, dob, status, case_ref, guardian_contact) VALUES
('Eli Okafor', 'Eridanus II', '2511-03-02', 'Closed - Deceased', 'OCPA-R4-11902', 'n.okafor@colonial-mail.eri2'),
('Talia Wren', 'Madrigal', '2511-05-19', 'Closed - Deceased', 'OCPA-R4-11944', 'r.wren@colonial-mail.mad'),
('Dominic Farrow', 'Skopje', '2510-11-30', 'Closed - Deceased', 'OCPA-R4-11887', 'unreachable - forwarding expired'),
('Priya Anand', 'Eridanus II', '2512-01-14', 'Active', 'OCPA-R4-12210', 'k.anand@colonial-mail.eri2'),
('Samuel Voight', 'Eridanus II', '2509-07-08', 'Closed - Deceased', 'OCPA-R4-10733', 'unreachable - forwarding expired');

-- Internal service credentials (lateral movement target)
CREATE TABLE service_accounts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    service_name VARCHAR(50),
    username VARCHAR(50),
    password VARCHAR(100),
    host VARCHAR(100),
    notes TEXT
);

INSERT INTO service_accounts (service_name, username, password, host, notes) VALUES
('CAIRN Fileshare', 'sysadmin', 'admin123', 'cairn.internal', 'Same login as the gateway account (reused, never rotated per-service)'),
('CAIRN Cache', '', '', 'cairn.internal:6379', 'No authentication required'),
('Gateway Maintenance SSH', 'backup', 'backup', 'relay.internal', 'Used for automated backups'),
('CAIRN Records Terminal', 'administrator', 'Records!Access99', 'cairn.internal:8080', 'Disposition/records interface, restricted');

-- Migration history (why LEDGER and CAIRN exist as separate tiers)
CREATE TABLE system_migration_log (
    id INT AUTO_INCREMENT PRIMARY KEY,
    entry_date VARCHAR(20),
    note TEXT
);

INSERT INTO system_migration_log (entry_date, note) VALUES
('2547-02-11', 'SPINDLE decommissioned. Active case records migrated to LEDGER. Long-term / restricted material migrated to CAIRN per disposition order.'),
('2547-02-11', 'Disposition authorized by ONI Section III liaison (Cmdr. I. Petrov). Access to CAIRN restricted to authorized personnel only.'),
('2547-02-14', 'Reminder: do not cross-reference SPINDLE transfer references against current dependent status without disposition clearance.');

-- Weak permissions: allow remote root login
GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' IDENTIFIED BY 'S3cretDB!2024' WITH GRANT OPTION;
GRANT ALL PRIVILEGES ON *.* TO 'app_svc'@'%' IDENTIFIED BY 'S3cretDB!2024';
FLUSH PRIVILEGES;
