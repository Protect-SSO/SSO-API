CREATE DATABASE SSO;

CREATE USER 'custom'@'localhost' IDENTIFIED BY 'custom';

USE SSO;

CREATE TABLE Users 
(UserName      varchar(100),
Password      varchar(100),
FirstName     varchar(100),
LastName      varchar(100),
Email         varchar(100),
AccountType   varchar(100),
Organization  varchar(100));

INSERT INTO Users(
  UserName     ,
  Password     ,
  FirstName    ,
  LastName     ,
  Email        ,
  AccountType  ,
  Organization
) VALUES
  ('user1'   , 'pw1'   , 'user'     , 'something' , 'email_1@gmail.com' , 'Owner'       , 'SSOBoys' ),
  ('user2'   , 'pw2'   , 'user2'     , 'something_else' , 'email_2@gmail.com' , 'Employee'    , 'SSOBoys1');

