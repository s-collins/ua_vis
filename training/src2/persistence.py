import mysql.connector
from datetime import datetime
import cv2 as cv


class Persistence:

    CREDENTIALS = {
        'user': 'vision',
        'password': 'vision',
        'host': 'localhost',
        'database': 'VisionData',
        'raise_on_warnings': True
    }

    PATH_ROOT = '/home/vis/Desktop/training_images/raw/'

    def __init__(self):
        try:
            self.cnx = mysql.connector.connect(**self.CREDENTIALS)
        except mysql.connector.Error as err:
            print(err)

    def __del__(self):
        self.cnx.close()

    def save(self, training_example):
        # save the image
        path = self.PATH_ROOT
        path = path + str(datetime.now()) + '.jpg'
        cv.imwrite(path, training_example.image)

        # save to training example table
        cursor = self.cnx.cursor()
        query = ("INSERT INTO TrainingExample "
                 "(image_filepath, camera_angle, camera_height, light_angle) "
                 "VALUES (%s, %s, %s, %s)")
        data = (path, training_example.camera_angle, training_example.camera_height, training_example.light_angle)
        cursor.execute(query, data)
        record_id = cursor.lastrowid

        # save the labels
        query = ("INSERT INTO Label "
                 "(image_id, x1, x2, y1, y2) "
                 "VALUES (%s, %s, %s, %s, %s)")
        for label in training_example.labels:
            x1 = label[0][0]
            x2 = label[1][0]
            y1 = label[0][1]
            y2 = label[1][1]
            data = (record_id, x1, x2, y1, y2)
            cursor.execute(query, data)

        cursor.close()
        self.cnx.commit()

