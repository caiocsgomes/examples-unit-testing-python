from my_cool_class import MyCoolClass


class TestMyCoolClass:
    def test_sum(self):
        cs = MyCoolClass()
        assert cs.sum(1, 2) == 3
