import papers
import sender

from time import sleep
from datetime import datetime, date, time, timedelta

def output_digest(recipients, keywords):
    ms = sender.MailSender(
        'server.example.com',
        'sender@example.com',
        'Hunter2',
        recipients
    )

    page = papers.Page.FromLink("astro-ph")

    article_list = page.get_interesting(keywords)

    message = "<h1>{}</h1>".format(page.title)
    for x in article_list:
        message += x.html

    ms.send_mail("ARXIV Digest: " + page.title, message)

def wait_until_next(t):
    tnext = datetime.combine(date.today() + timedelta(1), t)
    tdiff = tnext - datetime.now()
    
    sleep(int(tdiff.total_seconds()))

if __name__ == "__main__":
    output_digest(
        [
            ("Recipient #1", "recipient1@example.com"),
            ("Recipient #2", "recipient2@example.com")
        ],
        [
            "term1",
            "term2"
        ]
    )

    wait_until_next(6)