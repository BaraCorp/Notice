
try:
    # For Python 3.0 and later
    from urllib.request import urlopen
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen

from bs4 import BeautifulSoup

from django.core.management.base import BaseCommand
from job.models import NotClean
# from lxml import html


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):

        rps = self.anpe_mali()
        # self.stdout.write(self.style.SUCCESS(
        #     'Successfully {}'.format(rps)))

    def anpe_mali(self):
        url_base = "http://www.anpe-mali.org/offres-demploi/"
        html = urlopen(url_base).read()
        soup = BeautifulSoup(html, "html.parser")
        # print(soup)
        for ul in soup.find_all('article'):
            url_notice = url_base + ul.find('a').get('href')
            print("url notice : ", url_notice)
            try:
                page_art = urlopen(url_notice).read()
                spage_art = BeautifulSoup(page_art)
                secction = spage_art.find('section')
                data = {
                    'body': secction,
                }
                call_for_tender, ok = NotClean.objects.get_or_create(
                    url=url_notice, defaults=data)
            except Exception as e:
                print(e)
