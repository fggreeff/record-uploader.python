CREATE TABLE IF NOT EXISTS model.s3_files
(ID             varchar(36) PRIMARY KEY NOT NULL,
title           CHAR(10),
uploaded        CHAR(1)    NOT NULL,
row_updated_by  VARCHAR(150)  NOT NULL,
row_update_date TIMESTAMP,
file_reference   TEXT);