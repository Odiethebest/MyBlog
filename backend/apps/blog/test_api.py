from django.test import TestCase
from rest_framework.test import APIClient

class BlogInMemoryAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_blog_list(self):
        resp = self.client.get("/blog/")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertIn("posts", data)
        self.assertGreaterEqual(len(data["posts"]), 2)

    def test_blog_create_and_retrieve(self):
        payload = {"title": "Test Post", "content": "Hello"}
        resp = self.client.post("/blog/", payload, format="json")
        self.assertEqual(resp.status_code, 201)
        created = resp.json()
        self.assertIn("id", created)

        post_id = created["id"]
        resp2 = self.client.get(f"/blog/{post_id}/")
        self.assertEqual(resp2.status_code, 200)
        got = resp2.json()
        self.assertEqual(got["title"], "Test Post")
        self.assertEqual(got["content"], "Hello")

    def test_blog_update(self):
        create = self.client.post("/blog/", {"title": "A", "content": "B"}, format="json")
        post_id = create.json()["id"]

        resp = self.client.put(f"/blog/{post_id}/", {"title": "A2", "content": "B2"}, format="json")
        self.assertEqual(resp.status_code, 200)
        updated = resp.json()
        self.assertEqual(updated["title"], "A2")
        self.assertEqual(updated["content"], "B2")

    def test_blog_delete(self):
        create = self.client.post("/blog/", {"title": "Del", "content": "Me"}, format="json")
        post_id = create.json()["id"]

        resp = self.client.delete(f"/blog/{post_id}/")
        self.assertEqual(resp.status_code, 204)

        resp2 = self.client.get(f"/blog/{post_id}/")
        self.assertEqual(resp2.status_code, 404)

    def test_search(self):
        resp = self.client.get("/blog/search/?q=django&page=1&page_size=10")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertIn("posts", data)
        self.assertIn("total", data)
        self.assertIn("page", data)
        self.assertIn("page_size", data)

    def test_categories_and_posts(self):
        resp = self.client.get("/categories/")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertIn("categories", data)
        self.assertGreaterEqual(len(data["categories"]), 1)

        cat_id = data["categories"][0]["id"]
        resp2 = self.client.get(f"/categories/{cat_id}/posts/?page=1&page_size=10")
        self.assertEqual(resp2.status_code, 200)
        data2 = resp2.json()
        self.assertIn("posts", data2)
        self.assertIn("total", data2)

    def test_tags_and_posts(self):
        resp = self.client.get("/tags/")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertIn("tags", data)
        self.assertGreaterEqual(len(data["tags"]), 1)

        tag_id = data["tags"][0]["id"]
        resp2 = self.client.get(f"/tags/{tag_id}/posts/?page=1&page_size=10")
        self.assertEqual(resp2.status_code, 200)
        data2 = resp2.json()
        self.assertIn("posts", data2)
        self.assertIn("total", data2)

    def test_archives_and_posts(self):
        resp = self.client.get("/archives/")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertIn("archives", data)

        if data["archives"]:
            year = data["archives"][0]["year"]
            month = data["archives"][0]["month"]
            resp2 = self.client.get(f"/archives/{year}/{month}/posts/?page=1&page_size=10")
            self.assertEqual(resp2.status_code, 200)
            data2 = resp2.json()
            self.assertIn("posts", data2)
            self.assertIn("total", data2)