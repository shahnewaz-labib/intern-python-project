from getpass import getpass
from time import sleep

from pyjokes import get_joke

from util import (
    NetworkRequest,
    print_data,
    print_error,
    print_info,
    print_success,
    print_warning,
)


def token_refresh_decorator(func):
    def wrapper(self, *args, **kwargs):
        response = func(self, *args, **kwargs)

        if response["code"] == 401:
            self.refresh_tokens()

            self.headers["Authorization"] = f"Bearer {self.access_token}"
            response = func(self, *args, **kwargs)

        return response

    return wrapper


class TwitterBot:
    def __init__(self):
        self.api_base = "http://localhost:8000/api"
        self.username = None
        self.password = None
        self.access_token = None
        self.refresh_token = None
        self.headers = {"Content-Type": "application/json"}
        self.login()

    def login(self) -> None:
        print_info("Please login to your account")
        username = input("Username: ")
        password = getpass()

        self.username = username
        self.password = password

        print_warning("Logging in ...")

        try:
            login_data = {"username": username, "password": password}
            headers = {"Content-Type": "application/json"}
            response = NetworkRequest.post(
                f"{self.api_base}/auth", data=login_data, headers=headers
            )

            if response["code"] == 200:
                print_success("Login successful\n")
                self.access_token = response["body"]["access_token"]
                self.refresh_token = response["body"]["refresh_token"]
                self.headers["Authorization"] = f"Bearer {self.access_token}"
            else:
                print_error(
                    f"Login failed: {response.get('body').get('detail', 'Unknown error')}"
                )
                exit(1)
        except Exception as e:
            print_error(f"An error occurred during login: {e}")
            exit(1)

    def refresh_tokens(self) -> None:
        try:
            refresh_result = NetworkRequest.post(
                f"{self.api_base}/auth/token",
                data={"refresh_token": self.refresh_token},
                headers=self.headers,
            )

            if refresh_result["code"] == 200:
                print_warning("Token refreshed")
                self.access_token = refresh_result["body"]["access_token"]
                self.refresh_token = refresh_result["body"]["refresh_token"]
            else:
                print_error(
                    f"Failed to refresh token: {refresh_result.get('body', 'Unknown error')}"
                )
                exit(1)
        except Exception as e:
            print_error(f"An error occurred while refreshing the token: {e}")
            exit(1)

    def get_new_tweet(self, existing_tweets) -> str:
        while True:
            tweet = get_joke()
            if tweet not in existing_tweets:
                return tweet

    @token_refresh_decorator
    def post_tweet(self, tweet_data):
        try:
            post_result = NetworkRequest.post(
                f"{self.api_base}/tweets", data=tweet_data, headers=self.headers
            )
            return post_result

        except Exception as e:
            print_error(f"Error: {e}")
            exit(1)

    @token_refresh_decorator
    def check_recent_tweets(self):
        print_info("checking recent tweets ...\n")
        tweets_result = NetworkRequest.get(
            f"{self.api_base}/tweets", headers=self.headers
        )
        return tweets_result

    def run(self) -> None:
        print_info("\nTweets go brrr ...\n")
        tweets_result = self.check_recent_tweets()

        if tweets_result["code"] == 200:
            print_success(f"Time taken: {tweets_result['response_time']} seconds\n")
            print_info("Showing last 5 tweets ...")

            for tweet in tweets_result["body"][:5]:
                print_data(
                    f"({tweet['id']}) {tweet['author']['firstname'].title()} tweeted at {tweet['created_at']}\n {tweet['text']}",
                )
            tweets = set([tweet["text"] for tweet in tweets_result["body"]])

            for _ in range(10):
                tweet = self.get_new_tweet(tweets)
                tweet_data = {"text": tweet}
                post_result = self.post_tweet(tweet_data)
                if post_result["code"] == 201:
                    print_info(f"Tweeted: {tweet_data['text']}")
                    print_success(
                        f"Time taken: {post_result['response_time']} seconds\n"
                    )
                else:
                    print_error(
                        f"Failed to post tweet: {post_result.get('body', 'Unknown error')}"
                    )
                sleep(1)


def getNewTweet(existing_tweets) -> str:
    # NOTE: inifnite loop
    while True:
        tweet = get_joke()
        if tweet not in existing_tweets:
            return tweet


if __name__ == "__main__":
    bot = TwitterBot()
    bot.run()
