from locust import HttpUser, task, between

class FlaskAppUser(HttpUser):
    wait_time = between(1, 3)

    @task
    def load_homepage(self):
        self.client.get("/")

    @task
    def submit_movie_request(self):
        self.client.post("/", data={"name": "Test User", "genre": "Drama", "mood": "Relaxed"})