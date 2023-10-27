import time
import os
import instaloader
import dotenv
from datetime import datetime
from instaloader.exceptions import TwoFactorAuthRequiredException

dotenv.load_dotenv()

IG_USER = os.getenv("IG_USER", "")
IG_PASSWORD = os.getenv("IG_PASSWORD", "")

REFERENCE = datetime(2023, 10, 25, 13, 13, 26)
SLEEP_INTERVAL = 5


def notify() -> None:
    os.system("""afplay '/System/Library/Sounds/Hero.aiff'""")


class InstagramBot:
    def __init__(self):
        self.ig = instaloader.Instaloader()
        self.session_file = os.path.expanduser(
            f"~/.config/instaloader/session-{IG_USER}"
        )

    def login(self) -> None:
        try:
            self.ig.login(IG_USER, IG_PASSWORD)
        except TwoFactorAuthRequiredException:
            twofa_code = input(f"please enter 2FA challenge:")
            self.ig.two_factor_login(int(twofa_code))
        self.ig.save_session_to_file(self.session_file)


def main(user_to_watch: str = "outpostclimbing"):
    bot = InstagramBot()

    while True:
        print("Starting to Instagram watcher...")
        print(f" -- monitoring '{user_to_watch}'")
        posts_iterator = instaloader.Profile.from_username(
            bot.ig.context, user_to_watch
        ).get_posts()
        latest_post = next(posts_iterator)

        if latest_post.date == REFERENCE:
            print(f"{datetime.now().strftime('%d/%m/%Y %H:%M:%S')} - no updates")
        else:
            notify()
            print(f"UPDATED!!! {latest_post.date=}")

        time.sleep(SLEEP_INTERVAL)


if __name__ == "__main__":
    main()
