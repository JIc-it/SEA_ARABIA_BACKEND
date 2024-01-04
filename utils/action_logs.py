import json
from local_apps.api_report.models import ActionLog, ModelUpdateLog


def convert_string_to_dict(string):
    if string:
        try:
            # Replace single quotes with double quotes
            string = string.replace("'", "\"")

            # Use json.loads to convert the JSON string to a Python object
            value_list = json.loads(string)

            # Check if the value is a list
            if isinstance(value_list, list):
                # Wrap each dictionary in a list
                result_list = [item for item in value_list]
                return result_list
            else:
                print("Invalid JSON format: not a list")
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")

    return None


def create_log(user=None, model_name=None, action_value=None, title=None, value_before=None, value_after=None):
    user = user if user else None
    model_name = model_name if model_name else None
    action_value = action_value if action_value else None
    title = title if title else None
    value_before = value_before if value_before else None
    value_after = value_after if value_after else None

    # Convert the strings to dictionaries
    value_before_dict = convert_string_to_dict(value_before)
    value_after_dict = convert_string_to_dict(value_after)

    action_data = ActionLog(
        user=user,
        model_name=model_name,
        action=action_value,
        title=title,
        value_before=value_before_dict,
        value_after=value_after_dict
    )
    action_data.save()
    return True


def create_model_log(user=None, model_name=None, timestamp=None,
                     data_before=None, data_after=None):
    user = user if user else None
    model_name = model_name if model_name else None
    timestamp = timestamp if timestamp else None
    data_before = data_before if data_before else None
    data_after = data_after if data_after else None

    # Convert the strings to dictionaries
    data_before_dict = convert_string_to_dict(data_before)
    data_after_dict = convert_string_to_dict(data_after)

    action_data = ModelUpdateLog(
        user=user,
        model_name=model_name,
        timestamp=timestamp,
        data_before=json.dumps(data_before_dict) or None,
        data_after=json.dumps(data_after_dict) or None
    )
    action_data.save()
    return True
