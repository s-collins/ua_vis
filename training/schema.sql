CREATE TABLE Project (
	name VARCHAR(100),
	created_at TIMESTAMP NOT NULL DEFAULT current_timestamp,
	PRIMARY KEY (name)
);

CREATE TABLE TrainingExample (
	id INT AUTO_INCREMENT,
	file_path VARCHAR(200),
	camera_angle INT,
	light_angle INT,
	proj_name VARCHAR(100),
	PRIMARY KEY (ID),
	FOREIGN KEY (proj_name) REFERENCES Project(name)
);

CREATE TABLE Label (
	id INT AUTO_INCREMENT,
	image_id INT,
	x1 INT,
	x2 INT,
	y1 INT,
	y2 INT,
	PRIMARY KEY (id),
	FOREIGN KEY (image_id) REFERENCES TrainingExample(id)
);
