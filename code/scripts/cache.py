import argparse
import os

import redis

# Environment variables for Redis configuration
REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = os.getenv("REDIS_PORT")
REDIS_DB = os.getenv("REDIS_DB")


def load_arguments():
    """
    Parse and load command-line arguments for interacting with Redis.

    This function creates an argument parser to accept commands and patterns
    to perform operations on a Redis database.

    Positional Arguments:
        command (str): The operation to perform. Choices are:
            - 'list': List all keys that match a given pattern.
            - 'invalidate': Invalidate (delete) keys matching a given pattern.
        pattern (str): The pattern to use for matching Redis keys (e.g., 'user:*').

    Returns:
        argparse.Namespace: A namespace object containing the parsed arguments.

    Example:
        $ python script.py list "user:*"
        $ python script.py invalidate "cache:*"
    """
    parser = argparse.ArgumentParser(description="Redis commands.")

    parser.add_argument(
        "command",
        choices=["list", "invalidate"],
        help="Command to execute (list or invalidate).",
    )

    parser.add_argument(
        "pattern",
        help="Search pattern for matching Redis keys. For example, 'user:*'.",
    )

    return parser.parse_args()


def list_items(pattern: str) -> None:
    """
    List all Redis keys that match a given pattern.

    This function connects to a Redis database and retrieves all keys that
    match the provided pattern using the SCAN feature.

    Args:
        pattern (str): The pattern to search for in the Redis database.

    Returns:
        None: Prints the list of matched keys to the console.

    Example Output:
        ['user:1', 'user:2', 'user:3']

    Raises:
        redis.RedisError: If an error occurs when communicating with the Redis server.
    """
    redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)
    for entry in redis_client.scan_iter(pattern):
        print(entry)


def invalidate_cache(pattern: str) -> None:
    """
    Delete all Redis keys that match a given pattern.

    This function connects to a Redis database to invalidate (delete) all keys that match the provided pattern.

    Args:
        pattern (str): The pattern to search for in the Redis database.

    Returns:
        None: Prints the number of deleted Redis keys or a message if no keys were found.

    Raises:
        redis.RedisError: If an error occurs when communicating with the Redis server.

    Example Output:
        5 keys matching 'cache:*' were deleted.
    """
    redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)
    keys_to_delete = list(redis_client.scan_iter(pattern))
    if keys_to_delete:
        deleted_count = redis_client.delete(*keys_to_delete)
        print(f"{deleted_count} keys matching '{pattern}' were deleted.")
    else:
        print("No keys found with the given pattern.")


def main() -> None:
    """
    Main entry point of the script.

    This function parses command-line arguments using `load_arguments()`
    and executes the chosen Redis operation (`list` or `invalidate`)
    based on the input.

    Commands:
        - list: Retrieve all keys matching the specified pattern.
        - invalidate: Delete all keys matching the specified pattern.

    Returns:
        None
    """
    args = load_arguments()
    if args.command == "list":
        list_items(args.pattern)
    elif args.command == "invalidate":
        invalidate_cache(args.pattern)


if __name__ == "__main__":
    main()
