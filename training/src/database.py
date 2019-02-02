import mysql.connector
from datetime import datetime


class Database:

    CONFIG = {
        'user': 'vision',
        'password': 'vision',
        'host': 'localhost',
        'database': 'VisionData',
        'raise_on_warnings': True
    }

    FORMAT = '.jpg'

    def __init__(self):
        try:
            self.cnx = mysql.connector.connect(**self.CONFIG)
        except mysql.connector.Error as err:
            print(err)

    def __del__(self):
        self.cnx.close()

    def InsertProject(self, project):
        cursor = self.cnx.cursor()
        query = ('INSERT INTO Project'
                 '(name)'
                 'VALUES (%s)')
        data = (project.name)
        cursor.execute(query, data)
        cursor.close()
        self.cnx.commit()

    def InsertTrainingExample(self, example, project):
        cursor = self.cnx.cursor()

        # Save the Training Example attributes
        filepath = project.path + '/' + str(datetime.now()) + self.FORMAT
        query = ('INSERT INTO TrainingExample'
                 '(file_path, camera_angle, light_angle, proj_name)'
                 'VALUES (%s, %s, %s, %s)')
        data = (filepath, example.camera_angle, example.light_angle, proj_name)
        cursor.execute(query, data)

        # Get the ID of the inserted image
        record_id = cursor.lastrowid

        # Save all of the labels associated with the Training Example
        for label in example.labels:
            query = ('INSERT INTO Label'
                     '(image_id, x1, x2, y1, y2)'
                     'VALUES (%s, %s, %s, %s)')
            data = (record_id, label.x1, label.x2, label.y1, label.y2)
            cursor.execute(query, data)

        cursor.close()
        self.cnx.commit()

