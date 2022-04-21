# Practical examples of unit testing in python

This repository contains several scenarios of testing in python and it is meant as a cheat sheet to speed development of
tests.

The first thing we need to do is to install the pytest package:

```bash
pip install pytest
```

Pytest will take all the functions that start with *test_* inside modules that also start with *test_*, assume they are
tests and run them.

To run the test we would run the pytest at the project root folder:

````bash
pytest
````

## Test classes

A good structure would be if we have a class called *MyCoolClass*, that contains a method called *my_cool_method*,
inside a module called *my_cool_class*, for testing we would create a module called *test_my_cool_class* with a class
called *TestMyCoolClass* with a method called *test_my_cool_method*. For example:

[my_cool_class.py](https://github.com/caiocsgomes/examples-unit-testing-python/blob/main/my_cool_class.py)

```python
class MyCoolClass:
    def sum(self, a, b):
        return a + b
```

[test_my_cool_class.py](https://github.com/caiocsgomes/examples-unit-testing-python/blob/main/test_my_cool_class.py)

```python
class TestMyCoolClass:
    def test_sum(self):
        cs = MyCoolClass()
        assert cs.sum(1, 2) == 3
```

## Test functions

For functions we have the same structure removing the classes.

[my_methods.py](https://github.com/caiocsgomes/examples-unit-testing-python/blob/main/my_methods.py)

```python
def sum(a, b):
    return a + b
```

[test_my_methods.py](https://github.com/caiocsgomes/examples-unit-testing-python/blob/main/test_my_methods.py)

```python
def test_sum():
    assert sum(1, 2) == 3
```

## Test classes with external resources (connecting to APIs, DBs, etc)

Now lets say we have a method that retrieves data from an external resource, an API for example, during the tests we
don't want it to access the external API. If the API is down for example our test will break and this won't be due to
our code. In this case we have to mock the data. Mocking is the act of creating fake data for our tests.

For this test we will use the requests package:

```bash
pip install requests
```

[my_methods.py](https://github.com/caiocsgomes/examples-unit-testing-python/blob/main/my_methods.py)

````python
def is_user_birthday(id: int) -> bool:
    user = requests.get(f"fakeapi.com/{id}")
    today = datetime.today().strftime('%Y-%m-%d')
    return user['birthday'] == today
````

With *patch* we can pass a function we can mock, and then we define the return value we need inside the function we are
testing.

[test_my_methods.py](https://github.com/caiocsgomes/examples-unit-testing-python/blob/main/test_my_methods.py)

````python
@patch('my_methods.requests')
def test_is_user_birthday(mock_requests):
    today = datetime.today().strftime('%Y-%m-%d')
    mock_requests.get.return_value = {'birthday': today}
    assert is_user_birthday(1) == True
````

## Mock functions in return objects

In some cases the object returned by a function have methods used by the function and we need to include these methods
in the mock we create. The *json* method from the *Response* class is a good example. For this situation we can use
the *MagickMock* from the *unittest.Mock* and define the function inside the returned object.

[my_methods.py](https://github.com/caiocsgomes/examples-unit-testing-python/blob/main/my_methods.py)

````python
def get_user_age(id: int) -> str:
    user = requests.get(f"fakeapi.com/{id}")
    return user.json()['age']
````

In this example we are creating a *json* function in our mock that will always return the same.

[test_my_methods.py](https://github.com/caiocsgomes/examples-unit-testing-python/blob/main/test_my_methods.py)

````python
@patch('my_methods.requests')
def test_user_age(mock_requests):
    mock_requests.get.return_value = MagicMock(json=lambda: {'age': 10})
    assert get_user_age(1) == 10
````
