from locust import HttpUser, between, task, TaskSet


class PublicBeneficiariesSection(TaskSet):
    @task
    def public_list_beneficiaries(self):
        self.client.get(url="v1/pub/beneficiaries", headers={"accept": "application/json"})
        pass

    @task
    def public_list_beneficiaries_bnba(self):
        self.client.get(url="v1/pub/beneficiaries-bnba", headers={"accept": "application/json"})
        pass

    @task
    def stop(self):
        self.interrupt()


class ApiUser(HttpUser):
    wait_time = between(5, 15)
    tasks = {PublicBeneficiariesSection: 2}

    @task
    def ping(self):
        self.client.get(url="ping", headers={"accept": "application/json"})
        pass
