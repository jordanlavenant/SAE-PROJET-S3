import mysql.connector



try:
    connection = mysql.connector.connect(host='servinfo-maria',
                                         database='DBpilet',
                                         user='pilet',
                                         password='pilet')
    cursor = connection.cursor()
    # create table query
    create_table = """CREATE TABLE demo(id INT PRIMARY KEY,\
	name VARCHAR (255) NOT NULL, profile_pic LONGBLOB NOT NULL, \
	imp_files BLOB NOT NULL) """

    # Execute the create_table query first
    cursor.execute(create_table)
    # printing successful message
    print("Table created Successfully")

    query = """ INSERT INTO demo(id, name, profile_pic, imp_files)\
	VALUES (%s,%s,%s,%s)"""

    # First Data Insertion
    student_id = "1"
    student_name = "test"
    first_profile_picture = convert_data(
        "/media/o22201562/Colin/IUT/BUT2/SAE/devWeb/imageTest.jpg")
    first_text_file = convert_data(
        '/media/o22201562/Colin/IUT/BUT2/SAE/devWeb/test.txt')

    # Inserting the data in database in tuple format
    result = cursor.execute(
        query,
        (student_id, student_name, first_profile_picture, first_text_file))
    # Committing the data
    connection.commit()
    print("Successfully Inserted Values")

# Print error if occurred
except mysql.connector.Error as error:
    print(format(error))

finally:

    # Closing all resources
    if connection.is_connected():

        cursor.close()
        connection.close()
        print("MySQL connection is closed")
