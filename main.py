from getpass import getpass
from time import sleep
from typing import Tuple

from pyjokes import get_joke

from util import (
    NetworkRequest,
    print_data,
    print_error,
    print_info,
    print_success,
    print_warning,
)

API_BASE = "http://localhost:8000/api"


def login() -> Tuple[str, str]:
    print_info("Please login to your account")
    username = input("Username: ")
    password = getpass()

    print_warning("Logging in ...")

    try:
        login_data = {"username": username, "password": password}
        headers = {"Content-Type": "application/json"}
        response = NetworkRequest.post(
            f"{API_BASE}/auth", data=login_data, headers=headers
        )

        if response["code"] == 200:
            print_success("Login successful\n")
            return response["body"]["access_token"], response["body"]["refresh_token"]
        else:
            print_error(
                f"Login failed: {response.get('body').get('detail', 'Unknown error')}"
            )
            exit(1)
    except Exception as e:
        print_error(f"An error occurred during login: {e}")
        exit(1)


def getNewTweet(existing_tweets) -> str:
    # NOTE: inifnite loop
    while True:
        tweet = get_joke()
        if tweet not in existing_tweets:
            return tweet


def main() -> None:
    access_token, refresh_token = login()

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}",
    }

    print_info("checking recent tweets ...\n")

    tweets_result = NetworkRequest.get(f"{API_BASE}/tweets", headers=headers)

    print_success(f"Time taken: {tweets_result['response_time']} seconds\n")

    print_info("Showing last 5 tweets ...")

    for tweet in tweets_result["body"]:
        print_data(
            f"({tweet['id']}) {tweet['author']['firstname'].title()} tweeted at {tweet['created_at']}\n {tweet['text']}",
        )

    tweets = set([tweet["text"] for tweet in tweets_result["body"]])

    print_info("\nTweets go brrr ...\n")

    for _ in range(10):
        tweet = getNewTweet(tweets)
        tweet_data = {"text": tweet}

        post_result = None

        try:
            post_result = NetworkRequest.post(
                f"{API_BASE}/tweets", data=tweet_data, headers=headers
            )

            if post_result["code"] == 401:
                token_refresh_result = NetworkRequest.post(
                    f"{API_BASE}/auth/token",
                    data={"refresh_token": refresh_token},
                    headers=headers,
                )

                if token_refresh_result["code"] == 200:
                    print_warning("Token refreshed")
                    access_token = token_refresh_result["body"]["access_token"]
                    refresh_token = token_refresh_result["body"]["refresh_token"]

                    headers["Authorization"] = f"Bearer {access_token}"

                    post_result = NetworkRequest.post(
                        f"{API_BASE}/tweets", data=tweet_data, headers=headers
                    )

            if post_result["code"] == 201:
                print_info(f"Tweeted: {tweet}")
                print_success(f"Time taken: {post_result['response_time']} seconds\n")
            else:
                print_error(
                    f"Failed to post tweet: {post_result.get('body', 'Unknown error')}"
                )

        except Exception as e:
            print_error(f"Error: {e}")

        sleep(1)


if __name__ == "__main__":
    main()
