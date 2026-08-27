CREATE DATABASE IF NOT EXISTS one_stop_solutions
  CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE one_stop_solutions;

CREATE TABLE IF NOT EXISTS contact_submissions (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(120) NOT NULL,
  phone VARCHAR(20) NOT NULL,
  email VARCHAR(160) NOT NULL,
  service VARCHAR(120) NOT NULL,
  message TEXT,
  from_station VARCHAR(120),
  to_station VARCHAR(120),
  journey_date VARCHAR(20),
  return_date VARCHAR(20),
  passengers VARCHAR(10),
  email_sent VARCHAR(10) DEFAULT 'no',
  whatsapp_sent VARCHAR(10) DEFAULT 'no',
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
-- If you already have this table from before, either drop and recreate it,
-- or run: ALTER TABLE contact_submissions
--   MODIFY email VARCHAR(160) NOT NULL,
--   ADD COLUMN from_station VARCHAR(120),
--   ADD COLUMN to_station VARCHAR(120),
--   ADD COLUMN journey_date VARCHAR(20),
--   ADD COLUMN return_date VARCHAR(20),
--   ADD COLUMN passengers VARCHAR(10);

CREATE TABLE IF NOT EXISTS feedback (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(120) NOT NULL,
  service VARCHAR(60) NOT NULL,
  rating INT NOT NULL,
  message TEXT NOT NULL,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
-- service values: 'Accounting Services' | 'PAN Card and Other Services' | 'Travel Booking Services'
-- Powers the homepage testimonials bar (GET /api/feedback/top -> top 5 by rating).
