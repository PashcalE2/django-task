import datetime
from typing import Any
from faker import Faker
from django.db import models, transaction

from videos.models import Video
from users.models import User

import logging


logger = logging.getLogger(__name__)


class IFaker:
    def __init__(self, cls: models.Model, faker: Faker, number: int):
        self.cls = cls
        self.faker = faker
        self.number = number
        self.fakes = []

        self.batch_count = 1000

    def _fake_one(self) -> Any: ...

    def __next_fakes(self, count):
        self.fakes.extend([self._fake_one() for _ in range(count)])

    def apply(self):
        count = self.number
        cum_count = 0
        while count > 0:
            batch_count = min(count, self.batch_count)
            self.__next_fakes(batch_count)
            count -= batch_count
            cum_count += batch_count
            logger.info(f"Created {cum_count} / {self.number} fake objects")
        self.cls.objects.bulk_create(self.fakes)


class UserFaker(IFaker):
    def __init__(self, faker: Faker, number: int):
        super().__init__(User, faker, number)
        self.username_num = 0
        self.password_hash = "pbkdf2_sha256$1200000$CvcgrjbAGJWW3IdMweUUoz$ZiTLPv0N7T0R3lsLK9hCheS8124tPyuCYRZcIrmVWvw="

        logger.info("Deleting rows from User")
        User.objects.exclude(username="admin").delete()
        logger.info("Done")

    def _fake_one(self):
        self.username_num += 1
        return User(
            username=f"user{self.username_num}",
            password=self.password_hash,
            first_name="first_name",  # self.faker.first_name(),
            last_name="last_name",  # self.faker.last_name(),
            email="email@email.com",  # self.faker.email(),
            is_staff=False,  # self.faker.boolean(),
        )


class VideoFaker(IFaker):
    def __init__(self, faker: Faker, number: int, user_fakes: list[User]):
        super().__init__(Video, faker, number)
        self.user_fakes = user_fakes

    def _fake_one(self):
        return Video(
            owner=self.faker.random_element(self.user_fakes),
            is_published=False,  # self.faker.boolean(),
            name="name",  # self.faker.text(max_nb_chars=50),
            total_likes=0,
            created_at=datetime.datetime.now(),  # self.faker.date_time(),
        )


def main(commit, users_count, videos_count):
    logger.info("Data WILL be commited" if commit else "Data will NOT be commited")
    logger.info(f"Users count = {users_count}")
    logger.info(f"Videos count = {videos_count}")
    faker = Faker()

    try:
        with transaction.atomic():
            user_faker = UserFaker(faker, users_count)
            user_faker.apply()

            video_faker = VideoFaker(faker, videos_count, user_fakes=user_faker.fakes)
            video_faker.apply()

            if not commit:
                raise Exception("Was NOT commited")
    except Exception as e:
        logger.warning(str(e))


def run(*args):
    logging.basicConfig(
        level=logging.INFO,
        format="[%(asctime)s] [%(name)s] [%(levelname)s]: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    timeit_ = "timeit" in args
    commit = "commit" in args

    splitted = [arg.split("=") for arg in args]

    users_count = 1
    for val in (int(split[1]) for split in splitted if split[0] == "users"):
        users_count = val
        break

    videos_count = 1
    for val in (int(split[1]) for split in splitted if split[0] == "videos"):
        videos_count = val
        break

    def main_():
        main(commit, users_count, videos_count)

    if timeit_:
        import timeit

        logger.info(f"Execution time = {timeit.timeit(main_, number=1)}")
    else:
        main_()
