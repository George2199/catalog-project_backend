import unittest
from app import app, db
from models import Resource

class ResourceApiTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        self.ctx = app.app_context()
        self.ctx.push()

        self.resource = Resource(
            title="Test Resource",
            url="https://example.com",
            section="Test Section",
            tags="test,example",
            description="Test Description",
            contact_info="test@example.com",
            user_id=1
        )
        db.session.add(self.resource)
        db.session.commit()

    def tearDown(self):
        db.session.delete(self.resource)
        db.session.commit()
        self.ctx.pop()

    def test_get_resource(self):
        response = self.app.get(f'/api/resources/{self.resource.id}')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["title"], "Test Resource")

    def test_get_nonexistent_resource(self):
        response = self.app.get('/api/resources/999999')
        self.assertEqual(response.status_code, 404)

    def test_create_resource(self):
        new_data = {
            "title": "New Resource",
            "url": "https://new.com",
            "section": "Education",
            "tags": "flask,test",
            "description": "Demo",
            "contact_info": "email@example.com",
            "user_id": 1
        }
        response = self.app.post('/api/resources/', json=new_data)
        self.assertEqual(response.status_code, 201)
        self.assertIn("id", response.get_json())

    def test_update_resource(self):
        updated = {"title": "Updated Title"}
        response = self.app.put(f'/api/resources/{self.resource.id}', json=updated)
        self.assertEqual(response.status_code, 200)

        # Проверим обновлённый ресурс
        updated_res = db.session.get(Resource, self.resource.id)
        self.assertEqual(updated_res.title, "Updated Title")

    def test_delete_resource(self):
        # сначала создаём отдельный ресурс
        to_delete = Resource(
            title="ToDelete",
            url="https://x.com",
            section="X",
            tags="x",
            description="x",
            contact_info="x",
            user_id=1
        )
        db.session.add(to_delete)
        db.session.commit()

        res_id = to_delete.id
        response = self.app.delete(f'/api/resources/{res_id}')
        self.assertEqual(response.status_code, 200)

        # убедимся, что удалён
        self.assertIsNone(Resource.query.get(res_id))

if __name__ == '__main__':
    unittest.main()
