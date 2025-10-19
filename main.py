import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dance_school.settings')

django.setup()

from repositories.RepositoryManager import RepositoryManager

if __name__ == "__main__":
    repo = RepositoryManager()

    print("All clients:")
    all_clients = repo.clients.get_all()
    for c in all_clients:
     print(f"{c.name} {c.surname}")

    print("\nClient id=1:")
    client = repo.clients.get_by_id(1)
    print(client)

    print("\nClient:")
    client = repo.clients.get_by_name("Ava", "Moore")
    print(client.email)

    # new_client = repo.clients.add(
    #     name="Bob",
    #     surname="Smith",
    #     phone="0123456789",
    #     email="bob@example.com",
    #     subscription_id=3
    # )


    # deleted = repo.clients.delete(14)

    print("All halls:")
    all_halls = repo.halls.get_all()
    for h in all_halls:
        print(f"{h.name}, capacity: {h.capacity}")

    print("\nHall id=1:")
    hall = repo.halls.get_by_id(1)
    print(hall)

    # new_hall = repo.halls.add(name="Small Hall", capacity=20)
    # new_hall = repo.halls.add(name="Big Hall", capacity=20)
    # hall = repo.halls.add_equipment(hall_id=9, equipment_ids=[1, 2])

    # updated_hall = repo.halls.update(1, capacity=50)

    # deleted = repo.halls.delete(9)

    # print("Attendance:")
    # all_att = repo.attendances.get_all()
    # for a in all_att:
    #     print(a)
    #
    # print("\nAttendance id=1:")
    # attendance = repo.attendances.get_by_id(1)
    # print(attendance)

    # new_attendance = repo.attendances.add(date="2025-10-08", class_id=1, client_id=1)

    # deleted = repo.attendances.delete(32)