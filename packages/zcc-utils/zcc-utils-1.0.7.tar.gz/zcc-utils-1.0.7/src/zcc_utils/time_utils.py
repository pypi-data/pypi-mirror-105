import time

def second_to_minute(second: int):
    """
    秒转分钟
    :param second: 秒 int
    :return: 分钟 float
    """
    return second / 60


def second_to_hour(second: int):
    """
    秒转小时
    :param second: 秒 int
    :return: 小时 float
    """
    return second / 60 / 60


if __name__ == "__main__":
    print(time.localtime(1620557507))
