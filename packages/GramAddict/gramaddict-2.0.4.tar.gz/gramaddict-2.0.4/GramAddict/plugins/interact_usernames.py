from GramAddict.core.handle_sources import interact
from GramAddict.core.filter import Filter
import logging
from functools import partial
from colorama import Style
from os import path
from random import shuffle
from GramAddict.core.decorators import run_safely
from GramAddict.core.plugin_loader import Plugin
from GramAddict.core.views import TabBarView
from GramAddict.core.utils import (
    get_value,
)
from GramAddict.core.interaction import (
    _on_interaction,
    interact_with_user,
    is_follow_limit_reached_for_source,
)

logger = logging.getLogger(__name__)


class InteractUsernames(Plugin):
    """Interact with users that are given from a file"""

    def __init__(self):
        super().__init__()
        self.description = "Interact with users that are given from a file"
        self.arguments = [
            {
                "arg": "--aainteract-from-file",
                "nargs": "+",
                "help": "filenames of the list of users [*.txt]",
                "metavar": ("filename1", "filename2"),
                "default": None,
                "operation": True,
            }
        ]

    def run(self, device, configs, storage, sessions, plugin):
        class State:
            def __init__(self):
                pass

            is_job_completed = False

        self.args = configs.args
        self.device_id = configs.args.device
        self.sessions = sessions
        self.session_state = sessions[-1]
        profile_filter = Filter(storage)
        self.current_mode = plugin

        file_list = [file for file in (self.args.interact_from_file)]
        shuffle(file_list)

        for file in file_list:
            limit_reached = self.session_state.check_limit(
                self.args, limit_type=self.session_state.Limit.ALL
            )

            self.state = State()
            logger.info(f"Handle {file}", extra={"color": f"{Style.BRIGHT}"})

            on_interaction = partial(
                _on_interaction,
                likes_limit=int(self.args.total_likes_limit),
                source=file,
                interactions_limit=get_value(
                    self.args.interactions_count, "Interactions count: {}", 70
                ),
                sessions=self.sessions,
                session_state=self.session_state,
                args=self.args,
            )

            def get_int_from_percentage_ranges(
                stories_range, follow_range, comment_range, interact_range
            ):
                stories_percentage = get_value(
                    stories_range, "Chance of watching stories: {}%", 40
                )
                follow_percentage = get_value(
                    follow_range, "Chance of following: {}%", 40
                )
                comment_percentage = get_value(
                    comment_range, "Chance of commenting: {}%", 40
                )
                interact_percentage = get_value(
                    interact_range, "Chance of interacting: {}%", 40
                )
                return (
                    stories_percentage,
                    follow_percentage,
                    comment_percentage,
                    interact_percentage,
                )

            (
                stories_percentage,
                follow_percentage,
                comment_percentage,
                interact_percentage,
            ) = get_int_from_percentage_ranges(
                self.args.stories_percentage,
                self.args.follow_percentage,
                self.args.comment_percentage,
                self.args.interact_percentage,
            )

            @run_safely(
                device=device,
                device_id=self.device_id,
                sessions=self.sessions,
                session_state=self.session_state,
                screen_record=self.args.screen_record,
                configs=configs,
            )
            def job():
                self.handle_username_file(
                    device,
                    file,
                    self.args.likes_count,
                    self.args.stories_count,
                    stories_percentage,
                    follow_percentage,
                    int(self.args.follow_limit) if self.args.follow_limit else None,
                    comment_percentage,
                    interact_percentage,
                    self.args.scrape_to_file,
                    plugin,
                    storage,
                    profile_filter,
                    on_interaction,
                )
                self.state.is_job_completed = True

            while not self.state.is_job_completed and not limit_reached:
                job()

            if limit_reached:
                logger.info("Likes and follows limit reached.")
                self.session_state.check_limit(
                    self.args, limit_type=self.session_state.Limit.ALL, output=True
                )
                break

    def handle_username_file(
        self,
        device,
        current_file,
        likes_count,
        stories_percentage,
        follow_percentage,
        follow_limit,
        comment_percentage,
        interact_percentage,
        scraping_file,
        current_job,
        storage,
        profile_filter,
        on_like,
        on_watch,
        on_interaction,
    ):
        interaction = partial(
            interact_with_user,
            my_username=self.session_state.my_username,
            likes_count=likes_count,
            stories_percentage=stories_percentage,
            follow_percentage=follow_percentage,
            comment_percentage=comment_percentage,
            on_like=on_like,
            on_watch=on_watch,
            profile_filter=profile_filter,
            args=self.args,
            session_state=self.session_state,
            scraping_file=scraping_file,
            current_mode=self.current_mode,
        )

        is_follow_limit_reached = partial(
            is_follow_limit_reached_for_source,
            follow_limit=follow_limit,
            source=current_file,
            session_state=self.session_state,
        )

        need_to_refresh = True
        if path.isfile(current_file):
            with open(current_file, "r") as f:
                for line in f:
                    username = line.strip()
                    if username != "":
                        if storage.is_user_in_blacklist(username):
                            logger.info(f"@{username} is in blacklist. Skip.")
                            continue
                        elif storage.check_user_was_interacted(username):
                            logger.info(f"@{username}: already interacted. Skip.")
                            continue
                        if need_to_refresh:
                            search_view = TabBarView(device).navigateToSearch()
                        profile_view = search_view.navigateToUsername(
                            username, True, need_to_refresh
                        )
                        need_to_refresh = False
                        if not profile_view:
                            continue

                        if not interact(
                            storage,
                            is_follow_limit_reached,
                            username,
                            interaction,
                            device,
                            self.session_state,
                            current_job,
                            on_interaction,
                        ):
                            return
                        device.back()
                    else:
                        logger.info("Line in file is blank, skip.")
                remaining = f.readlines()
            if self.args.delete_interacted_users:
                with open(current_file, "w", encoding="UTF-8") as f:
                    f.writelines(remaining)
        else:
            logger.warning(f"File {current_file} not found.")
            return

        logger.info(f"Interact with users in {current_file} complete.")
        device.back()
