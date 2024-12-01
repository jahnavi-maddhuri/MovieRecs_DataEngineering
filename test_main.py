from app import add


def test_add():
    """testing out add"""
    assert add(3, 5) == 8
    assert add(2, 2) == 4
    assert add(1, 2) == 3
    print("Success")


def test_add2():
    assert add(1, 1) == 2
    assert add(0, 0) == 0
    print("Success 2")


if __name__ == "__main__":
    test_add()
    test_add2()
