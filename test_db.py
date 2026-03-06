import unittest
from Modals.User import USERS, User

class TestUsersTable(unittest.IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        await USERS.clear()

    async def asyncTearDown(self):
        pass

    async def test_add_user(self):
        # Test adding a user to the USERS table
        user_data = {
            "name": "John Doe",
            "email": "john.doe@example.com",
            "password": "securepassword",
            "avatar": "avatar.png",
            "role": "admin"
        }
        user = await USERS.add_user(**user_data)
        self.assertIsInstance(user, User)
        self.assertEqual(user.user_name, "John Doe")
        self.assertEqual(user.user_email, "john.doe@example.com")

    async def test_get_user(self):
        # Test retrieving a user by ID
        user_data = {
            "name": "2132",
            "email": "jane.doe@2132.com",
            "password": "2132",
            "avatar": "2132.png",
            "role": "user"
        }
        user = await USERS.add_user(**user_data)
        retrieved_user = await USERS.get(user.user_id)
        self.assertIsInstance(retrieved_user, User)
        self.assertEqual(retrieved_user.user_name, "2132")
        self.assertEqual(retrieved_user.user_email, "jane.doe@2132.com")

if __name__ == "__main__":
    unittest.main()