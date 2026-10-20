from tests.test_students_db import client
from tests.test_students_db import student_payload


# test 1 - list student test
def test_list_students():
    response = client.get("/students/")

    assert response.status_code == 200
    assert isinstance(response.json(),list)

# test 2 - create the student test
def test_create_student(student_payload):
    response = client.post("/students/",json=student_payload)

    assert response.status_code == 200
    assert response.json()["name"] == student_payload["name"]
    assert response.json()["age"] == student_payload["age"]
    assert response.json()["email"] == student_payload["email"]
    assert "id" in response.json()

# test 3 - get a student from id
def test_student_from_id(student_payload):
    response = client.post("/students/",json=student_payload)

    assert response.status_code == 200

    student_id = response.json()["id"]

    response = client.get(f"/students/{student_id}")

    assert response.status_code == 200
    assert response.json()["name"] == student_payload["name"]
    assert response.json()["age"] == student_payload["age"]
    assert response.json()["email"] == student_payload["email"]

# test 4 - test updated student 
def test_update_student(student_payload):
    response = client.post("/students/",json=student_payload)

    assert response.status_code == 200

    student_id = response.json()["id"]

    updated_payload= {
        "name": "Arun Kumar",
        "age": 23,
        "email": "arun.updated@example.com",
    }

    response = client.put(f"/students/{student_id}",json=updated_payload)

    assert response.json()["name"] == updated_payload["name"]
    assert response.json()["age"] == updated_payload["age"]
    assert response.json()["email"] == updated_payload["email"]

# test 5 - delete student by id

def test_delete_by_id(student_payload):
    response = client.post("/students/",json=student_payload)

    assert response.status_code == 200

    student_id = response.json()["id"]

    response = client.delete(f"/students/{student_id}")

    assert response.status_code == 200

    response = client.get(f"/students/{student_id}")

    assert response.status_code == 404

# test 6 - test the nonexistent student

def test_get_nonexistent_student():
    response = client.get("/students/999999")

    assert response.status_code == 404
    assert response.json()["detail"] == "student not found"

# test 7 - test the valid of email
def test_create_student_invalid_email(student_payload):
    invalid_payload = student_payload.copy()
    invalid_payload["email"] = "not-an-email"

    response = client.post("/students/", json=invalid_payload)

    assert response.status_code == 422

# Test 8 - test missing required field
def test_create_student_missing_name(student_payload):
    invalid_payload = student_payload.copy()
    invalid_payload.pop("name")

    response = client.post("/students/",json=invalid_payload)

    assert response.status_code == 422

# test 9 - test create student by negatve age
def test_create_student_by_negative_age(student_payload):
    negative_payload = student_payload.copy()
    negative_payload["age"] = -2

    response = client.post("/students/",json=negative_payload)

    assert response.status_code == 422

# test 10 - test create student by above limit
def test_create_student_by_positive_limit_age(student_payload):
    negative_payload = student_payload.copy()
    negative_payload["age"] = 121

    response = client.post("/students/",json=negative_payload)

    assert response.status_code == 422

# test 11 - test invalid emails during student update
def test_student_update_email(student_payload):

    response = client.post("/students/",json=student_payload)

    assert response.status_code == 200

    student_id = response.json()["id"]

    invalid_email = student_payload.copy()
    invalid_email["email"] = "bad-email"

    response = client.put(f"/students/{student_id}",json=invalid_email)

    assert response.status_code == 422

#test 12 - test data update after failed updates
def test_student_data_after_failed_updates(student_payload):

    response = client.post("/students/",json=student_payload)

    assert response.status_code == 200

    student_id = response.json()["id"]

    invalid_email = student_payload.copy()
    invalid_email["email"] = "bad-email"

    response = client.put(f"/students/{student_id}",json=invalid_email)

    assert response.status_code == 422

    response = client.get(f"/students/{student_id}")

    assert response.json()["email"] == student_payload["email"]

# test 13 - test the updated student with negative age
def test_update_student_with_negative_age(student_payload):
    response = client.post("/students/",json=student_payload)

    assert response.status_code == 200

    student_id = response.json()["id"]

    negative_age = student_payload.copy()
    negative_age["age"] = -5

    response = client.put(f"/students/{student_id}",json=negative_age)

    assert response.status_code == 422

# test 14 - test the updated student with upper limit age
def test_update_student_with_upper_limit_age(student_payload):
    response = client.post("/students/",json=student_payload)

    assert response.status_code == 200

    student_id = response.json()["id"]

    negative_age = student_payload.copy()
    negative_age["age"] = 121

    response = client.put(f"/students/{student_id}",json=negative_age)

    assert response.status_code == 422

# test 15 - test create a student with duplicate data
def test_create_student_with_duplicate_data(student_payload):
    response = client.post("/students/",json=student_payload)

    assert response.status_code == 200

    response = client.post("/students/",json=student_payload)

    assert response.status_code == 409

# test 16 - test non exited student update
def test_update_nonexist_student(student_payload):
    response = client.put("/students/9999999",json=student_payload)

    assert response.status_code == 404
    assert response.json()["detail"] == "student not found"

# test 17 -test delete non existent student
def test_delete_nonexistent_student():
    response = client.delete("/students/999999")

    assert response.status_code == 404
    assert response.json()["detail"] == "student not found"

# test 18 - test create a stuent with missing age and email
def test_create_student_missing_age_and_email(student_payload):
    missing_value_data = student_payload.copy()
    missing_value_data.pop("age")
    missing_value_data.pop("email")

    response = client.post("/students/",json=missing_value_data)

    assert response.status_code == 422

# test 19 - test Create a student with an invalid age typ
def test_Create_a_student_with_an_invalid_age_typ(student_payload):
    invalid_age = student_payload.copy()
    invalid_age["age"] = "twenty"

    response = client.post("/students/",json=invalid_age)

    assert response.status_code == 422


# test 20 - test student list after creating and deleting a student
def test_student_list_after_create_and_delete(student_payload):
    # Create a student
    response = client.post("/students/", json=student_payload)

    assert response.status_code == 200

    student_id = response.json()["id"]

    # Check that the student appears in the list
    response = client.get("/students/")

    assert response.status_code == 200

    students = response.json()

    assert any(student["id"] == student_id for student in students)

    # Delete the student
    response = client.delete(f"/students/{student_id}")

    assert response.status_code == 200

    # Check that the student no longer appears in the list
    response = client.get("/students/")

    assert response.status_code == 200

    students = response.json()

    assert not any(student["id"] == student_id for student in students)