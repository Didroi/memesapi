import allure


class SmallChecks:
    @allure.step('Check equals')
    def correct_equals(self):
        return 2 == 2

    @allure.step('Check equals')
    def incorrect_equals(self):
        return 2 != 2
