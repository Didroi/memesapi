import requests
import allure
from tests import BaseApi
from tests import url


class DeletePost(BaseApi):
    @allure.step('Delete Post')
    def delete_object(self, object_id):

        self.response = requests.delete(
            f'{url.url}/{object_id}'
        )

    @allure.step('Check right answer in response')
    def deletion_confirm(self):
        return 'has been deleted' in str(self.response.json())
