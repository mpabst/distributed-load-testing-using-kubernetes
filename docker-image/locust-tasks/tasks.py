from locust import HttpLocust, TaskSet, task
# import pydevd as pydevd


class UserBehavior(TaskSet):

    @task(1)
    def loadUser(self):
        self.client.headers['Content-Type'] = "application/json"
        self.client.headers['Authorization'] = "Bearer " + self.token
        query_string = "{user(id: " + str(self.id) + "){id,firstName, lastName, photos {id, thumbnailUrl, url}}}"
        print(query_string)
        self.client.post("/graphql", json={"query": query_string})

    @task(1)
    def photoSearch(self):
        self.client.headers['Content-Type'] = "application/json"
        self.client.headers['Authorization'] = "Bearer " + self.token
        query_string = "{photoExploreSearch(requestingUser: " + str(self.id) + ", userOnly: false, exifStrings: [\"canon\"], industries: [100,101,102], tags: [100,101,102]) {count, id, thumbnailUrl, url}}"
        print(query_string)
        self.client.post("/graphql", json={"query": query_string})

    def on_start(self):
 #       pydevd.settrace('localhost', port=12345, stdoutToServer=True, stderrToServer=True)
        self.client.headers['Content-Type'] = "application/json"
        response = self.client.post("/graphql", json={"query": "mutation {login(email:\"robert@robertreich.co\", password:\"1234567A\"){ access_token, userId}}"})
        json_response_dict = response.json()
        self.token = json_response_dict['data']['login']['access_token']
        self.id = json_response_dict['data']['login']['userId']


class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 5000
    max_wait = 9000
