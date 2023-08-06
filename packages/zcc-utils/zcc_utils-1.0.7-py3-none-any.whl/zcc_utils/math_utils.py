def get_after_point_number(number: float):
    """
    获取小数点后的数，
    :return: 小数点后的数字 string
    """
    s1_list = str(number).split('.')
    return s1_list[1]


if __name__ == "__main__":
    print(get_after_point_number(1.2))
