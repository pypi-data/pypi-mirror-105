import itertools
import json
import logging
import re
from datetime import datetime
from json import JSONDecodeError
from typing import Any, Dict, Optional
from urllib.parse import parse_qs, urlparse

from . import utils
from .constants import FB_BASE_URL, FB_MOBILE_BASE_URL
from .fb_types import Options, Post, RawPost, RequestFunction, Response, URL


try:
    from youtube_dl import YoutubeDL
    from youtube_dl.utils import ExtractorError
except ImportError:
    YoutubeDL = None


logger = logging.getLogger(__name__)

# Typing
PartialPost = Optional[Dict[str, Any]]


def extract_post(raw_post: RawPost, options: Options, request_fn: RequestFunction) -> Post:
    return PostExtractor(raw_post, options, request_fn).extract_post()


def extract_group_post(raw_post: RawPost, options: Options, request_fn: RequestFunction) -> Post:
    return GroupPostExtractor(raw_post, options, request_fn).extract_post()


class PostExtractor:
    """Class for Extracting fields from a FacebookPost"""

    likes_regex = re.compile(r'([\d.KM]+)\s+(Like|left reaction)', re.IGNORECASE)
    comments_regex = re.compile(r'([\d,.KM]+)\s+comment', re.IGNORECASE)
    shares_regex = re.compile(r'([\d,.KM]+)\s+Share', re.IGNORECASE)
    live_regex = re.compile(r'.+(is live).+')
    link_regex = re.compile(r"href=\"https:\/\/lm\.facebook\.com\/l\.php\?u=(.+?)\&amp;h=")

    photo_link = re.compile(r'href=\"(/[^\"]+/photos/[^\"]+?)\"')
    photo_link_2 = re.compile(r'href=\"(/photo.php[^\"]+?)\"')
    image_regex = re.compile(
        r'<a href=\"([^\"]+?)\" target=\"_blank\" class=\"sec\">View Full Size<\/a>',
        re.IGNORECASE,
    )
    image_regex_lq = re.compile(r"background-image: url\('(.+)'\)")
    video_thumbnail_regex = re.compile(r"background: url\('(.+)'\)")
    post_url_regex = re.compile(r'/story.php\?story_fbid=')
    video_post_url_regex = re.compile(r'/.+/videos/.+/(.+)/.+')
    video_id_regex = re.compile(r'{&quot;videoID&quot;:&quot;([0-9]+)&quot;')

    shares_and_reactions_regex = re.compile(
        r'<script nonce=.*>.*bigPipe.onPageletArrive\((?P<data>\{.*RelayPrefetchedStreamCache.*\})\);'
        '.*</script>'
    )
    bad_json_key_regex = re.compile(r'(?P<prefix>[{,])(?P<key>\w+):')

    more_url_regex = re.compile(r'(?<=…\s)<a href="([^"]+)')
    post_story_regex = re.compile(r'href="(\/story[^"]+)" aria')

    def __init__(self, element, options, request_fn):
        self.element = element
        self.options = options
        self.request = request_fn

        self._data_ft = None

    # TODO: This is getting ugly, create a dataclass for Post
    def make_new_post(self) -> Post:
        return {
            'post_id': None,
            'text': None,
            'post_text': None,
            'shared_text': None,
            'time': None,
            'image': None,
            'image_lowquality': None,
            'images': None,
            'images_description': None,
            'images_lowquality': None,
            'images_lowquality_description': None,
            'video': None,
            'video_thumbnail': None,
            'video_id': None,
            'likes': None,
            'comments': None,
            'shares': None,
            'post_url': None,
            'link': None,
            'user_id': None,
            'username': None,
            'user_url': None,
            'source': None,
            'is_live': False,
            'factcheck': None,
            'shared_post_id': None,
            'shared_time': None,
            'shared_user_id': None,
            'shared_username': None,
            'shared_post_url': None,
            'available': None,
            'comments_full': None,
            'reactors': None,
            'w3_fb_url': None,
        }

    def extract_post(self) -> Post:
        """Parses the element into self.item"""

        methods = [
            self.extract_post_id,
            self.extract_text,
            self.extract_time,
            self.extract_photo_link,
            self.extract_image_lq,
            self.extract_likes,
            self.extract_comments,
            self.extract_shares,
            self.extract_post_url,
            self.extract_link,
            self.extract_user_id,
            self.extract_username,
            self.extract_video,
            self.extract_video_thumbnail,
            self.extract_video_id,
            self.extract_is_live,
            self.extract_factcheck,
            self.extract_share_information,
            self.extract_availability,
        ]

        post = self.make_new_post()
        post['source'] = self.element

        # TODO: this is just used by `extract_reactions`, probably should not be acceded from self
        self.post = post

        def log_warning(msg, *args):
            post_id = self.post.get('post_id', 'unknown post')
            logger.warning(f"[%s] {msg}", post_id, *args)

        for method in methods:
            try:
                partial_post = method()
                if partial_post is None:
                    log_warning("Extract method %s didn't return anything", method.__name__)
                    continue

                post.update(partial_post)
            except Exception as ex:
                log_warning("Exception while running %s: %r", method.__name__, ex)

        if self.options.get('reactions') or self.options.get('reactors'):
            try:
                reactions = self.extract_reactions()
            except Exception as ex:
                log_warning("Exception while extracting reactions: %r", ex)
                reactions = {}

            if reactions is None:
                log_warning("Extract reactions didn't return anything")
            else:
                post.update(reactions)

        if self.options.get('comments'):
            try:
                comments = self.extract_comments_full()
                post.update(comments)
                if post.get("comments_full") and not post.get("comments"):
                    post["comments"] = len(post.get("comments_full"))

            except Exception as ex:
                log_warning("Exception while extracting comments: %r", ex)

        return post

    def extract_post_id(self) -> PartialPost:
        return {'post_id': self.data_ft.get('top_level_post_id')}

    def extract_username(self) -> PartialPost:
        elem = self.element.find('h3 strong a', first=True)
        if elem:
            url = elem.attrs.get("href")
            if url:
                url = utils.urljoin(FB_BASE_URL, url)
            return {'username': elem.text, 'user_url': url}

    # TODO: this method needs test for the 'has more' case and shared content
    def extract_text(self) -> PartialPost:
        # Open this article individually because not all content is fully loaded when skimming
        # through pages.
        # This ensures the full content can be read.

        element = self.element

        has_more = self.more_url_regex.search(element.html)
        if has_more and self.options.get("allow_extra_requests", True):
            match = self.post_story_regex.search(element.html)
            if match:
                url = utils.urljoin(FB_MOBILE_BASE_URL, match.groups()[0].replace("&amp;", "&"))
                response = self.request(url)
                element = response.html.find('.story_body_container', first=True)

        nodes = element.find('p, header, span[role=presentation]')
        if nodes:
            post_text = []
            shared_text = []
            ended = False
            for node in nodes[1:]:
                if node.tag == 'header':
                    ended = True

                # Remove '... More'
                # This button is meant to display the hidden text that is already loaded
                # Not to be confused with the 'More' that opens the article in a new page
                if node.tag == 'p':
                    node = utils.make_html_element(
                        html=node.html.replace('>… <', '><', 1).replace('>More<', '', 1)
                    )

                if not ended:
                    post_text.append(node.text)
                else:
                    shared_text.append(node.text)

            # Separation between paragraphs
            paragraph_separator = '\n\n'

            text = paragraph_separator.join(itertools.chain(post_text, shared_text))
            post_text = paragraph_separator.join(post_text)
            shared_text = paragraph_separator.join(shared_text)

            return {
                'text': text,
                'post_text': post_text,
                'shared_text': shared_text,
            }

        return None

    # TODO: Add the correct timezone
    def extract_time(self) -> PartialPost:
        # Try to extract time for timestamp
        page_insights = self.data_ft.get('page_insights', {})

        for page in page_insights.values():
            try:
                timestamp = page['post_context']['publish_time']
                logger.debug(f"Got exact timestamp from publish_time: {datetime.fromtimestamp(timestamp)}")
                return {
                    'time': datetime.fromtimestamp(timestamp),
                }
            except (KeyError, ValueError):
                continue

        # Try to extract from the abbr element
        date_element = self.element.find('abbr', first=True)
        if date_element is not None:
            date = utils.parse_datetime(date_element.text, search=False)
            if date:
                return {'time': date}
            logger.debug("Could not parse date: %s", date_element.text)
        else:
            logger.warning("Could not find the abbr element for the date")

        # Try to look in the entire text
        date = utils.parse_datetime(self.element.text)
        if date:
            return {'time': date}

        return None

    def extract_user_id(self) -> PartialPost:
        return {'user_id': self.data_ft['content_owner_id_new']}

    def extract_image_lq(self) -> PartialPost:
        elems = self.element.find('div.story_body_container>div .img:not(.profpic):not([style*="static.xx.fbcdn.net"])')
        images = []
        descriptions = []
        for elem in elems:
            if elem.attrs.get('src'):
                images.append(elem.attrs.get('src'))
            elif elem.attrs.get('style'):
                match = self.image_regex_lq.search(elem.attrs.get('style'))
                if match:
                    src = utils.decode_css_url(match.groups()[0])
                    images.append(src)
            descriptions.append(elem.attrs.get("aria-label") or elem.attrs.get("alt"))

        image = images[0] if images else None
        return {"image_lowquality": image, "images_lowquality": images, "images_lowquality_description": descriptions}

    def extract_link(self) -> PartialPost:
        match = self.link_regex.search(self.element.html)
        if match:
            return {'link': utils.unquote(match.groups()[0])}
        return None

    def extract_post_url(self) -> PartialPost:

        query_params = ('story_fbid', 'id')
        account = self.options.get('account')
        elements = self.element.find('a')
        video_post_match = None
        path = None

        for element in elements:
            href = element.attrs.get('href', '')

            post_match = self.post_url_regex.match(href)
            video_post_match = self.video_post_url_regex.match(href)

            if post_match:
                path = utils.filter_query_params(href, whitelist=query_params)

            elif video_post_match:
                video_post_id = video_post_match.group(1)

                if account is None:
                    path = f'watch?v={video_post_id}'
                else:
                    path = f'{account}/videos/{video_post_id}'

        post_id = self._data_ft.get('top_level_post_id')

        if video_post_match is None and account is not None and post_id is not None:
            path = f'{account}/posts/{post_id}'

        if path is None:
            return None

        url = utils.urljoin(FB_BASE_URL, path)
        return {'post_url': url}

    # TODO: Remove `or 0` from this methods
    def extract_likes(self) -> PartialPost:
        return {
            'likes': utils.find_and_search(
                self.element, 'footer', self.likes_regex, utils.convert_numeric_abbr
            )
            or 0,
        }

    def extract_comments(self) -> PartialPost:
        return {
            'comments': utils.find_and_search(
                self.element, 'footer', self.comments_regex, utils.convert_numeric_abbr
            )
            or 0,
        }

    def extract_shares(self) -> PartialPost:
        return {
            'shares': utils.find_and_search(
                self.element, 'footer', self.shares_regex, utils.convert_numeric_abbr
            )
            or 0,
        }

    def extract_photo_link_HQ(self, response: Response) -> URL:
        # Find a link that says "View Full Size"
        match = self.image_regex.search(response.text)
        if match:
            url = match.groups()[0].replace("&amp;", "&")
            if not url.startswith("http"):
                url = utils.urljoin(FB_MOBILE_BASE_URL, url)
            if url.startswith(utils.urljoin(FB_MOBILE_BASE_URL, "/photo/view_full_size/")):
                # Try resolve redirect
                logger.debug(f"Fetching {url}")
                redirect_response = self.request(url)
                if not redirect_response.url.startswith(utils.urljoin(FB_MOBILE_BASE_URL, "login.php")):
                    url = redirect_response.html.find("a", first=True).attrs.get("href").replace("&amp;", "&")
            return url
        else:
            return None

    def extract_photo_link(self) -> PartialPost:
        if not self.options.get("allow_extra_requests", True):
            return None
        images = []
        descriptions = []
        photo_links = self.element.find("div.story_body_container>div a[href*='photo.php'],a[href*='/photos/']")
        total_photos_in_gallery = len(photo_links)
        if len(photo_links) == 4 and photo_links[-1].text:
            total_photos_in_gallery = 4 + int(photo_links[-1].text.strip("+")) - 1
            logger.debug(f"{total_photos_in_gallery} total photos in gallery")

        # This gets up to 4 images in gallery
        for link in photo_links:
            url = link.attrs["href"]
            if "photoset_token" in url:
                query = parse_qs(urlparse(url).query)
                photo_id = query["photo"][0]
                profile_id = query["profileid"][0]
                url = f"/photo.php?fbid={photo_id}&profileid={profile_id}"

            url = utils.urljoin(FB_MOBILE_BASE_URL, url)
            logger.debug(f"Fetching {url}")
            response = self.request(url)
            images.append(self.extract_photo_link_HQ(response))
            elem = response.html.find(".img[data-sigil='photo-image']", first=True)
            descriptions.append(elem.attrs.get("alt") or elem.attrs.get("aria-label"))

        while len(images) < total_photos_in_gallery:
            # More photos to fetch. Follow the left arrow link of the last image we were on
            url = response.html.find('a.touchable[data-gt=\'{"tn":"+>"}\']', first=True).attrs["href"]
            if not url.startswith("http"):
                url = utils.urljoin(FB_MOBILE_BASE_URL, url)
            logger.debug(f"Fetching {url}")
            response = self.request(url)
            images.append(self.extract_photo_link_HQ(response))
            elem = response.html.find(".img[data-sigil='photo-image']", first=True)
            descriptions.append(elem.attrs.get("alt") or elem.attrs.get("aria-label"))
        image = images[0] if images else None
        return {"image": image, "images": images, "images_description": descriptions}

    def extract_reactions(self) -> PartialPost:
        """Fetch share and reactions information with a existing post obtained by `get_posts`.
        Return a merged post that has some new fields including `reactions`, `w3_fb_url`,
        `fetched_time`, and reactions fields `LIKE`, `ANGER`, `SORRY`, `WOW`, `LOVE`, `HAHA` if
        exist.
        Note that this method will raise one http request per post, use it when you want some more
        information.

        Example:
        ```
        for post in get_posts('fanpage'):
            more_info_post = fetch_share_and_reactions(post)
            print(more_info_post)
        ```
        """
        url = self.post.get('post_url')
        post_id = self.post.get('post_id')
        w3_fb_url = url and utils.urlparse(url)._replace(netloc='www.facebook.com').geturl()

        reaction_url = f'https://m.facebook.com/ufi/reaction/profile/browser/?ft_ent_identifier={post_id}'
        response = self.request(reaction_url)
        reactions = {}

        # Dict mapping class names to human readable reaction names. Prepopulated in case FB doesn't include them
        reaction_lookup = {
            'sx_cbd149': 'Like',
            'sx_202991': 'Love',
            'sx_41edbc': 'Care',
            'sx_0d839a': 'Haha',
            'sx_2b1a8e': 'Wow',
            'sx_454e38': 'Angry',
            'sx_1a0b4b': 'Sad'
        }

        for span in response.html.find("span[aria-label]"):
            label = span.attrs.get("aria-label", "")
            if " people reacted with " in label:
                reaction_count, reaction_type = label.split(" people reacted with ")
                reactions[reaction_type.lower()] = utils.convert_numeric_abbr(reaction_count)
                if self.options.get("reactors"):
                    emoji_class = span.find("i", first=True).attrs.get("class")[-1]
                    reaction_lookup[emoji_class] = reaction_type

        reactors = []

        reactors_opt = self.options.get("reactors")
        if reactors_opt:
            """Fetch people reacting to an existing post obtained by `get_posts`.
            Note that this method may raise one more http request per post to get all reactors"""
            limit = 3000
            if type(reactors_opt) in [int, float] and reactors_opt < limit:
                limit = reactors_opt
            logger.debug(f"Fetching {limit} reactors")
            elems = list(response.html.find("div#reaction_profile_browser>div"))
            more = response.html.find("div#reaction_profile_pager a", first=True)
            if more and limit > 50:
                url = utils.urljoin(FB_MOBILE_BASE_URL, more.attrs.get("href"))
                url = url.replace("limit=50", f"limit={limit - 50}")
                logger.debug(f"Fetching {url}")
                response = self.request(url)
                prefix_length = len('for (;;);')
                data = json.loads(response.text[prefix_length:])  # Strip 'for (;;);'

                for action in data['payload']['actions']:
                    if action['cmd'] == 'append':
                        html = utils.make_html_element(f"<div id='reaction_profile_browser'>{action['html']}</div>", url=FB_MOBILE_BASE_URL)
                        more_elems = html.find('div#reaction_profile_browser>div')
                        elems.extend(more_elems)
            logger.debug(f"Found {len(elems)} reactors")
            for elem in elems:
                emoji_class = elem.find("div>i:not(.nub)", first=True).attrs.get("class")[-1]
                if not reaction_lookup.get(emoji_class):
                    logger.error(f"Don't know {emoji_class}")
                reactors.append({
                    "name": elem.find("strong", first=True).text,
                    "link": utils.urljoin(FB_BASE_URL, elem.find("a", first=True).attrs.get("href")),
                    "type": reaction_lookup.get(emoji_class)
                })

        if reactions:
            return {
                'likes': reactions.get("like"),
                'reactions': reactions,
                'reactors': reactors,
                'fetched_time': datetime.now(),
                'w3_fb_url': w3_fb_url,
            }

        if url:
            resp = self.request(w3_fb_url)
            for item in self.parse_share_and_reactions(resp.text):
                data = item['jsmods']['pre_display_requires'][0][3][1]['__bbox']['result'][
                    'data'
                ]['feedback']
                if data['subscription_target_id'] == post_id:
                    return {
                        'shares': data['share_count']['count'],
                        'likes': data['reactors']['count'],
                        'reactions': {
                            reaction['node']['reaction_type'].lower(): reaction['reaction_count']
                            for reaction in data['top_reactions']['edges']
                        },
                        'comments': data['comment_count']['total_count'],
                        'w3_fb_url': data['url'],
                        'fetched_time': datetime.now(),
                    }
        return None

    def extract_video(self):
        video_data_element = self.element.find('[data-sigil="inlineVideo"]', first=True)
        if video_data_element is None:
            return None
        if self.options.get('youtube_dl'):
            vid = self.extract_video_highres()
            if vid:
                return vid
        return self.extract_video_lowres(video_data_element)

    def extract_video_lowres(self, video_data_element):
        try:
            data = json.loads(video_data_element.attrs['data-store'])
            return {'video': data.get('src').replace("\\/", "/")}
        except JSONDecodeError as ex:
            logger.error("Error parsing data-store JSON: %r", ex)
        except KeyError:
            logger.error("data-store attribute not found")
        return None

    def extract_video_highres(self):
        if not YoutubeDL:
            raise ModuleNotFoundError(
                "youtube-dl must be installed to download videos in high resolution."
            )

        ydl_opts = {
            'format': 'best',
            'quiet': True,
        }
        if self.options.get('youtube_dl_verbose'):
            ydl_opts['quiet'] = False

        try:
            post_id = self.post.get('post_id')
            if post_id is None:
                return None

            video_page = 'https://www.facebook.com/' + post_id
            with YoutubeDL(ydl_opts) as ydl:
                url = ydl.extract_info(video_page, download=False)['url']
                return {'video': url}
        except ExtractorError as ex:
            logger.error("Error extracting video with youtube-dl: %r", ex)

        return None

    def extract_video_thumbnail(self):
        thumbnail_element = self.element.find('i[data-sigil="playInlineVideo"]', first=True)
        if not thumbnail_element:
            return None
        style = thumbnail_element.attrs.get('style', '')
        match = self.video_thumbnail_regex.search(style)
        if match:
            return {'video_thumbnail': utils.decode_css_url(match.groups()[0])}
        return None

    def extract_video_id(self):
        match = self.video_id_regex.search(self.element.html)
        if match:
            return {'video_id': match.groups()[0]}
        return None

    def extract_is_live(self):
        header = self.element.find('header')[0].full_text

        match = self.live_regex.search(header)

        if match is not None:
            return {'is_live': True}

        return {'is_live': False}

    def extract_factcheck(self):
        button = self.element.find('button[value="See Why"]', first=True)
        if not button:
            return None
        factcheck_div = button.element.getparent().getparent()
        factcheck = ""
        for text in factcheck_div.itertext():
            if text.strip() == "See Why":
                continue
            factcheck += text + "\n"
        return {'factcheck': factcheck}

    def extract_share_information(self):
        if not self.data_ft.get("original_content_id"):
            return None
        logger.debug(
            "%s is a share of %s", self.post["post_id"], self.data_ft["original_content_id"]
        )
        # A shared post contains an <article> element within it's own <article> element, or a header element for a shared image
        raw_post = self.element.find(
            "article article, .story_body_container .story_body_container header", first=True
        )
        # We can re-use the existing parsers, as a one level deep recursion
        shared_post = PostExtractor(raw_post, self.options, self.request)
        return {
            'shared_post_id': self.data_ft["original_content_id"],
            'shared_time': shared_post.extract_time().get("time"),
            'shared_user_id': self.data_ft["original_content_owner_id"],
            'shared_username': shared_post.extract_username().get("username"),
            'shared_post_url': shared_post.extract_post_url().get("post_url"),
        }

    def extract_availability(self):
        return {
            'available': ">This content isn't available at the moment<" not in self.element.html
        }

    def parse_comment(self, comment):
        comment_id = comment.attrs.get("id")

        profile_picture = comment.find(".profpic.img", first=True)
        name = profile_picture.attrs.get("alt") or profile_picture.attrs.get("aria-label")
        name = name.split(",")[0]

        url = profile_picture.element.getparent().attrib.get("href")
        if url:
            url = utils.urljoin(FB_BASE_URL, url)

        first_link = comment.find("div:not([data-sigil])>a[href]:not([data-click]):not([data-store]):not([data-sigil])", first=True)
        comment_body_elem = comment.find('[data-sigil="comment-body"]', first=True)
        commenter_meta = None
        if first_link:
            if "\n" in first_link.text:
                commenter_meta = first_link.text.split("\n")[0]

        text = comment_body_elem.text
        # Try to extract from the abbr element
        date_element = comment.find('abbr', first=True)
        if date_element:
            date = utils.parse_datetime(date_element.text, search=False)
        else:
            date = None

        return {
            "comment_id": comment_id,
            "commenter_url": url,
            "commenter_name": name,
            "commenter_meta": commenter_meta,
            "comment_text": text,
            "comment_time": date,
        }

    def extract_comments_full(self):
        """Fetch comments for an existing post obtained by `get_posts`.
        Note that this method may raise multiple http requests per post to get all comments"""
        url = self.post.get('post_url').replace(FB_BASE_URL, FB_MOBILE_BASE_URL)
        logger.debug(f"Fetching {url}")
        response = self.request(url)
        elem = response.html.find('div[data-sigil="m-mentions-expand"]', first=True)
        if not elem:
            logger.warning("No comments found on page")
            return
        comments = list(elem.find('div[data-sigil="comment"]'))
        limit = 5000
        comments_opt = self.options.get('comments')
        if type(comments_opt) in [int, float]:
            limit = comments_opt
        more = elem.find("a", containing="View more comments", first=True)
        while more and len(comments) < limit:
            url = utils.urljoin(FB_MOBILE_BASE_URL, more.attrs.get("href"))
            logger.debug(f"Fetching {url}")
            response = self.request(url)
            elem = response.html.find('div[data-sigil="m-mentions-expand"]', first=True)
            if not elem:
                logger.warning("No comments found on page")
                break
            more_comments = elem.find('div[data-sigil="comment"]')
            comments.extend(more_comments)
            more = response.html.find("a", containing="View more comments", first=True)

        logger.debug(f"Found {len(comments)} comments")
        results = []
        for comment in comments:
            result = self.parse_comment(comment)
            replies = comment.find("div.async_elem[data-sigil='replies-see-more'] a[href]", first=True)
            if replies:
                logger.debug(f"{result['comment_id']} has replies")
                url = utils.urljoin(FB_MOBILE_BASE_URL, replies.attrs["href"])
                logger.debug(f"Fetching {url}")
                response = self.request(url)
                replies = response.html.find('div[data-sigil="comment"]')
                result["replies"] = [self.parse_comment(reply) for reply in replies[1:]] # Skip first element, as it will be this comment itself
            results.append(result)
        return {"comments_full": results}

    def parse_share_and_reactions(self, html: str):
        bad_jsons = self.shares_and_reactions_regex.findall(html)
        for bad_json in bad_jsons:
            good_json = self.bad_json_key_regex.sub(r'\g<prefix>"\g<key>":', bad_json)
            yield json.loads(good_json)

    @property
    def data_ft(self) -> dict:
        if self._data_ft is not None:
            return self._data_ft

        self._data_ft = {}
        try:
            data_ft_json = self.element.attrs['data-ft']
            self._data_ft = json.loads(data_ft_json)
        except JSONDecodeError as ex:
            logger.error("Error parsing data-ft JSON: %r", ex)
        except KeyError:
            logger.error("data-ft attribute not found")

        return self._data_ft


class GroupPostExtractor(PostExtractor):
    """Class for extracting posts from Facebook Groups rather than Pages"""
    post_url_regex = re.compile(r'https://m.facebook.com/groups/[^/]+/permalink/')
    post_story_regex = re.compile(r'href="(https://m.facebook.com/groups/[^/]+/permalink/\d+/)')
