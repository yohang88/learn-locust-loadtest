from locust import between, task, TaskSet
from locust.contrib.fasthttp import FastHttpUser
import json

class AuthenticateAdminSection(TaskSet):
    auth_token = None

    def login(self):
        data = {"LoginForm": {"username": "staffkotabandung", "password": "123456"}}
        response = self.client.post("v1/staff/login", data=json.dumps(data), headers={"accept": "application/json","content-type": "application/json"})
        if response:
            response_json = response.json()
            self.auth_token = response_json['data']['access_token']
        pass

    def on_start(self):
        self.login()

    @task
    def get_profile(self):
        if self.auth_token:
            self.client.get("v1/staff/me", headers={"accept": "application/json", "authorization": f"Bearer {self.auth_token}"})
        pass

    @task
    def stop(self):
        self.interrupt()

class PublicBeneficiariesSection(TaskSet):
    # @task
    # def public_list_beneficiaries(self):
    #     self.client.get("v1/pub/beneficiaries", headers={"accept": "application/json"})
    #     pass
    #
    # @task
    # def public_list_beneficiaries_bnba(self):
    #     self.client.get("v1/pub/beneficiaries-bnba", headers={"accept": "application/json"})
    #     pass

    @task
    def public_list_beneficiaries_bnba_statistic_area(self):
        self.client.get("v1/pub/beneficiaries-bnba/statistics-by-area", headers={"accept": "application/json"})
        pass

    @task
    def stop(self):
        self.interrupt()


class ApiUser(FastHttpUser):
    wait_time = between(5, 15)
    tasks = {PublicBeneficiariesSection: 10}

    # @task
    # def ping(self):
    #     self.client.get("ping", headers={"accept": "application/json"})
    #     pass
