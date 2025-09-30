import re


def format_date(date_str):
    day, month, year = date_str.split("-")
    return f"{year}/{month}/{day}"


def format_phone(phone_str):
    phone_str = re.sub(r"[()\-]", " ", phone_str)
    phone_str = re.sub(r"\s+", " ", phone_str)
    phone_str = phone_str.strip()
    parts = phone_str.split()
    formatted_phone = f"{' '.join(parts[:-2])}-{parts[-2]}{parts[-1]}"
    return formatted_phone


def extract_username(email):
    return email.split("[at]")[0]


def main(table):
    table = list(
        filter(lambda row: row[0] is not None and row[1] is not None, table)
    )

    transformed_table = []
    for row in table:
        date_part, phone_part = row[0].split("!")
        email = row[1]

        formatted_date = format_date(date_part)
        formatted_phone = format_phone(phone_part)
        username = extract_username(email)

        transformed_table.append([formatted_date, formatted_phone, username])
    transformed_table.sort(key=lambda x: x[2])
    transformed_table = list(map(list, zip(*transformed_table)))

    return transformed_table
