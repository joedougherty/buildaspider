import concurrent.futures
from datetime import datetime
from enum import Enum
import logging
import os
import re
import sys
from urllib.parse import urljoin


from bs4 import BeautifulSoup

import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry


from spiderconfig import Config


class LinkStatus(Enum):
    OK = 1
    BROKEN = 2
    RAISED_EXCEPTION = 3


class Link(object):
    def __init__(self, context, href, text, cfg, status=LinkStatus.OK):
        self.context = context
        self.href = self._handle_href(href)
        self.text = text
        self.cfg = cfg
        self.worth_visiting = self._worth_visiting()
        self.status = status
        self.http_code = None
        self.err_msg = None

    def _handle_href(self, href):
        href = href.strip()

        # Rewrite relative links so we can visit them!
        if href.startswith(("/", "../")):
            href = urljoin(self.context, href)
        return href

    def _worth_visiting(self):
        if any([re.search(url, self.href) for url in self.cfg.include_patterns]):
            return True
        elif any([re.search(url, self.href) for url in self.cfg.exclude_patterns]):
            return False
        else:
            return False

    def __hash__(self):
        return hash(hash(self.context) + hash(self.href) + hash(self.text))

    def __repr__(self):
        return f"""{self.href}
  - with text: "{self.text}"
  - appearing on: {self.context}"""


def mint_new_session():
    adapter = HTTPAdapter(max_retries=Retry(total=3, backoff=1))
    session = requests.Session()
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session


def check_link(session_link_tuple):
    session, link = session_link_tuple

    try:
        resp = session.get(link.href)
    except Exception as e:
        link.status, link.err_msg = LinkStatus.RAISED_EXCEPTION, e
        return link

    if resp.status_code in (200, 201, 302):
        status = LinkStatus.OK
    else:
        status = LinkStatus.BROKEN

    link.status, link.http_code = status, resp.status_code

    return link


class Spider(object):
    def __init__(
        self,
        path_to_config_file,
        verbose=False,
        max_workers=8,
        time_format="%Y-%m-%d_%H:%M",
    ):
        self.verbose = verbose
        self.cfg = Config(path_to_config_file)
        self.max_workers = max_workers
        self.time_format = time_format

        self.visit_queue = list()

        self.visited_urls = set()
        self.checked_urls = set()
        self.broken_urls = set()
        self.exception_urls = set()

        if all((self.cfg.username, self.cfg.password, self.cfg.login_url)):
            self.session = self.login()
        else:
            self.session = mint_new_session()

    def _update(self, checked_link):
        self.checked_urls.add(checked_link.href)

        if checked_link.status == LinkStatus.OK:
            if checked_link.worth_visiting:
                self.visit_queue.append(checked_link)

            self.log_checked_link(link)
        elif checked_link.status == LinkStatus.BROKEN:
            self.broken_urls.add(link.href)
            self.log_broken_link(link)
        elif checked_link.status == LinkStatus.RAISED_EXCEPTION:
            self.exception_urls.add(link.href)
            self.log_exception_link(link)
        else:
            self.status_logger.error(
                f"._update() received checked_link: {checked_link}"
            )

    def setup_logging(self):
        now = datetime.now().strftime(self.time_format)

        logging.basicConfig(
            filename=os.path.join(self.cfg.log_dir, "spider_{}.log".format(now)),
            level=logging.INFO,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        )

        self.status_logger = logging.getLogger(__name__)

        self.broken_links_logpath = os.path.join(
            self.cfg.log_dir, "broken_links_{}.log".format(now)
        )
        self.checked_links_logpath = os.path.join(
            self.cfg.log_dir, "checked_links_{}.log".format(now)
        )
        self.exception_links_logpath = os.path.join(
            self.cfg.log_dir, "exception_links_{}.log".format(now)
        )

    def login(self):
        raise NotImplementedError

    def log_checked_link(self, link):
        raise NotImplementedError

    def log_broken_link(self, link):
        raise NotImplementedError

    def log_exception_link(self, link):
        raise NotImplementedError

    def keep_link(self, href):
        if any(
            (
                href in self.broken_urls,
                href in self.exception_urls,
                href in self.visited_urls,
            )
        ):
            return False
        else:
            return True

    def gather_links(self, markup, current_url):
        gathered_links = list()

        for elem in BeautifulSoup(markup, "html.parser").find_all("a"):
            try:
                href = elem["href"]
            except KeyError:
                # Skip any <a> tags missing the "href" attribute.
                continue

            if href != current_url and self.keep_link(href):
                gathered_links.append(
                    Link(current_url, href, elem.text, cfg=self.cfg)
                )

        return gathered_links

    def visit(self, link):
        self.status_logger.info("\nVisiting {}...".format(link.href))

        resp = self.session.get(link.href)
        self.visited_urls.add(link.href)

        gathered_links = self.gather_links(resp.content, link.href)
        self.status_logger.info("=> Checking {} links...".format(len(gathered_links)))

        packaged_links = [(self.session, link) for link in gathered_links]

        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as exe:
            for result in exe.map(check_link, packaged_links):
                self._update(result)

        self.status_logger.info(
            "Unique Pages Visited: {}".format(len(self.visited_urls))
        )
        self.status_logger.info(
            "Unique Links Checked: {}".format(len(self.checked_urls))
        )
        self.status_logger.info(
            "Broken Links Found: {}".format(len(self.broken_urls))
        )
        self.status_logger.info(
            "Pages in Visit Queue: {}".format(len(self.visit_queue))
        )

    def run(self):
        """
        Add the seed URLs specified in the config to the visit_queue.

        While the visit_queue is non-empty:

            + Visit the next page

            + Gather links on said page
                - Filter out: 
                    * visited URLs
                    * broken URLs
                    * URLs that caused exceptions

            + Check the gathered links:
                - Sort into:
                    * broken URLs
                    * URLs that caused exceptions
                - Add each to self.checked_urls

            + Add pertinent links to the visit_queue
        """
        for seed_url in self.cfg.seed_urls:
            self.visit_queue.append(Link(None, seed_url, None, cfg=self.cfg))

        try:
            while self.visit_queue:
                self.visit(self.visit_queue.pop(0))
        finally:
            self.session.close()

            self.status_logger.info("Crawling complete.")
