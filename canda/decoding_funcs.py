import pandas
import cantools
from typing import List

def convert_to_bytes(hex_string: str) -> bytes:
    """Convert an hex string to bytes.

    Adds a leading `0` if the hex string contains an odd number of characters.

    This function is required since some hex strings are not byte aligned,
    i.e. they contain an odd number of characters.

    Args:
        hex_string (str): The hex string to convert.

    Returns:
        bytes: The bytes representation of the hex string.
    """
    splitted = hex_string.split(" ")

    for index, hex_byte in enumerate(splitted):
        if len(hex_byte) == 1:
            splitted[index] = "0" + hex_byte

    try:
        return bytes.fromhex(" ".join(splitted))
    except ValueError:
        print("Error converting hex string to bytes:", hex_string)
        return None


def decode_row(
    row: pandas.Series,
    can_database: cantools.database.can.Database,
    decodable_ids: List[int],
) -> pandas.Series:

    if row.id in decodable_ids:
        decoded_message = can_database.decode_message(int(row.id), row.bytes_contents)
        decoded_message["time"] = row.timestamp
        return decoded_message
    else:
        return None

def to_seconds_elapsed(timestamp, start_time):
    return (timestamp - start_time).total_seconds()

def decode_can_binary(
    raw_data: pandas.DataFrame, can_database: cantools.database.can.Database
) -> pandas.DataFrame:

    decoded_data: pandas.DataFrame = pandas.DataFrame()
    decodable_ids: List[int] = list(
        dict.fromkeys([message.frame_id for message in can_database.messages])
    )

    decoded_data["timestamp"] = raw_data["time"]
    decoded_data["id"] = raw_data["id"].apply(int, base=16)
    decoded_data["bytes_contents"] = raw_data["bytes"].apply(convert_to_bytes)
    decoded_data["decoded_contents"] = decoded_data.apply(
        lambda row: decode_row(row, can_database, decodable_ids), axis=1
    )
    #Might be useful to have the start time of the data. If the DBC is not complete, 
    # it might be useful to know when the data starts.
    raw_start_time = decoded_data["timestamp"][0]
    
    decoded_data = decoded_data.dropna()
    
    formatted_data: pandas.DataFrame = pandas.DataFrame(list(decoded_data["decoded_contents"]))
    start_time = formatted_data["time"][0]
    formatted_data["time"] = formatted_data["time"].apply(lambda x: to_seconds_elapsed(x, raw_start_time))
    formatted_data.set_index("time", inplace=True)

    return formatted_data

def find_unknown_ids(
    df: pandas.DataFrame, can_database: cantools.database.can.Database
) -> List[int]:
    """
    Find CAN ids that cannot be decoded by the database.

    This function is useful to find ids that haven't been
    documented yet.

    Args:
        df (pandas.DataFrame): A dataframe produced by this program's
            parsing module.
        can_database (cantools.database.can.Database): The CAN
            database used to decode CAN bus data.

    Returns:
        List[int]: A list of identifiers as integers.
    """

    all_ids = df["id"].apply(int, base=16).tolist()
    decodable_ids: List[int] = list(
        dict.fromkeys([message.frame_id for message in can_database.messages])
    )

    return list(set(all_ids) - set(decodable_ids))
