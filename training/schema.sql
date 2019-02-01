CREATE TABLE Project (
    name CHAR(100) NOT NULL,
    root_filepath CHAR(100),
    PRIMARY KEY (name)
);

CREATE TABLE TrainingExample (
    id INT NOT NULL AUTO_INCREMENT,
    project CHAR(100) NOT NULL,
    recorder CHAR(100),
    image_filepath CHAR(100),
    FOREIGN KEY (project) REFERENCES `Project`(`name`),
    PRIMARY KEY (id, project)
);
