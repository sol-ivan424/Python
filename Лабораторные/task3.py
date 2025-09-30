import re


def main(input_string):
    result = {}

    sections = re.findall(r"<section>.*?</section>", input_string, re.DOTALL)

    for section in sections:
        variable_match = re.search(r"variable\s*{([^}]*)}", section)
        values_match = re.search(r"==>\s*@'([^']*)'", section)

        if variable_match and values_match:
            variable_values = variable_match.group(1).split(";")
            variable_values = [
                int(value.strip().replace("#", ""))
                for value in variable_values
            ]

            variable_name = values_match.group(1).strip()
            result[variable_name] = variable_values

    return result