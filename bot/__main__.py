# Imports

import praw
import config
from saucenao_api import SauceNao
import time
import traceback

reddit = praw.Reddit(
    client_id=config.REDDIT_CLIENT_ID,
    client_secret=config.REDDIT_CLIENT_SECRET,
    password=config.REDDIT_PASSWORD,
    username=config.REDDIT_USERNAME,
    user_agent=config.REDDIT_USER_AGENT
)

sauce = SauceNao(config.SAUCENAO_API_KEY)


def check_post_id_in_file(id_to_check):
    file = open("postRespondedTo.txt", "r")
    ids = file.readlines()
    if id_to_check+"\n" in ids:
        file.close()
        return True
    else:
        file.close()
        return False


def add_post_id_to_file(id_to_add):
    file = open("postRespondedTo.txt", "a")
    file.write(id_to_add + "\n")
    file.close()


def check_mentions():
    unread_mentions = []
    for mention in reddit.inbox.unread(limit=None):
        if "u/sauce-robot" in mention.body:
            unread_mentions.append(mention)
    return unread_mentions


def image_search(url):
    images = sauce.from_url(url)
    best_image = images[0]
    return best_image


def output_message(image):
    if image.urls:
        title = image.title
        url = image.urls
        similarity = image.similarity
        footer = "\n\nThe reverse image search was made using sauceNAO."
        if similarity > 65:
            return "Title: " + title + "\n\nSimilarity: " + str(similarity) + "\n\nURL: " + url[0] + footer
        else:
            return "SauceNAO returned unsatisfactory result. Similarity was too low."
    else:
        return "SauceNAO returned unsatisfactory results. Either similarity was too low or missing url in the result."


def is_image(url):
    extensions = (".jpg", ".png", ".jpeg")
    if url.endswith(extensions):
        return True
    else:
        return False


def bot():
    for unread_mention in reddit.inbox.unread(limit=None):
        if "u/sauce-robot" in unread_mention.body:
            post_id = unread_mention.parent_id.split("_")[1]
            image_url = reddit.submission(post_id).url
            if not check_post_id_in_file(post_id):
                if is_image(image_url):
                    image_info = image_search(image_url)
                    unread_mention.reply(output_message(image_info))
                    unread_mention.mark_read()
                    add_post_id_to_file(post_id)
                else:
                    unread_mention.reply("No image in the post.")
                    unread_mention.mark_read()
                    add_post_id_to_file(post_id)
            else:
                unread_mention.reply("Somebody already called the bot in this post.")
                unread_mention.mark_read()


if __name__ == "__main__":
    print("Start")
    try:
        while True:
            bot()
            time.sleep(10)
    except Exception:
        print(traceback.format_exc())
