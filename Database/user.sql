CREATE USER 'custom'@'%' IDENTIFIED BY 'custom';

GRANT ALL PRIVILEGES ON *.* TO 'custom'@'%'
	WITH GRANT OPTION;
FLUSH PRIVILEGES;

