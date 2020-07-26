import configparser
import os


class Config(object):
    def __init__(self, abs_path_to_config_file):
        self.CONFIG_PATH = abs_path_to_config_file

        config = configparser.RawConfigParser()
        config.read(self.CONFIG_PATH)

        self.cfg = config["buildaspider"]

        self.login = self.cfg.getboolean("login", None)
        self.username = self.cfg.get("username", None)
        self.password = self.cfg.get("password", None)
        self.login_url = self.cfg.get("login_url", None)

        self.log_dir = self.set_log_dir()

        self.include_patterns = self.extract_patterns("include_patterns")
        self.exclude_patterns = self.extract_patterns("exclude_patterns")
        self.seed_urls = self.extract_patterns("seed_urls")

        self.max_num_retries = self.cfg.getint("max_num_retries", 5)

    def extract_patterns(self, config_section):
        raw_val = self.cfg.get(config_section, None)
        if not raw_val:
            raise Exception(
                f"""Please ensure that "{config_section}" contains at least one value!"""
            )

        return [p for p in raw_val.split("\n") if p not in ("", " ")]

    def set_log_dir(self):
        log_dir = self.cfg["log_dir"]
        if not os.path.exists(log_dir):
            raise FileNotFoundError(
                f"The log directory does not exist: {log_dir}"
            )
        return log_dir
