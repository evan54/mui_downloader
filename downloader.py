from importlib import reload
import config as c
import pandas as pd

import os
from pathlib import Path
import subprocess
import bs4
reload(c)

import ftplib


class Downloader:

    def __init__(self, earliest_date, latest_date):
        self.earliest_date = earliest_date
        self.latest_date = latest_date
        self.address = f'ftp://{c.FTP_ADDRESS}:{c.FTP_PORT}'

    def _download_links(self, address):
        """
        Given an ftp address it parses it and gets the links and datestamps in
        that folder
        """

        earliest_date = self.earliest_date
        latest_date = self.latest_date

        command = ['wget', '-O', '-', address]
        response = subprocess.run(command, stdout=subprocess.PIPE)
        text_response = response.stdout.decode()

        pre_start = text_response.index('<pre>')
        pre_end = text_response.index('</pre>')

        # get <pre>()</pre> block
        html_lines = text_response[pre_start:pre_end].split('\n')
        html_lines = html_lines[1:-1]

        links = []
        for line in html_lines:
            el = line.split()
            date = pd.Timestamp(' '.join(el[:4]))
            bs = bs4.BeautifulSoup(line, features='html5lib').find('a')
            href = bs.attrs['href']
            if latest_date > date > earliest_date and 'File' in line:
                links.append([href, date])

        return links

    def _download_new_files(self):
        """
        Go through each of the paths where the media remains
        """
        address = self.address

        links = []
        for path in c.MEDIA_PATHS:
            links.extend(self._download_links(f'{address}/{path}/'))

        return links

    def copy_files(self, destination_folder):
        """
        Get new files and copy them to the destination_folder
        """
        links = self._download_new_files()
        destination_pn = c.PICTURE_DIR / destination_folder
        os.makedirs(destination_pn, exist_ok=True)
        for link, date in links:
            name = link.split('/')[-1]
            destination_pnfn = destination_pn / name
            command = ['wget', '-O', destination_pnfn.as_posix(), link]

            # copy file
            subprocess.run(command, stdout=subprocess.PIPE)

            # delete old file
            link_split = link.split('/')
            name = link_split[-1]
            cwd = '/' + '/'.join(link_split[3:-1])
            ftp.cwd(cwd)
            ftp.delete(name)


def run_files():
    year = Path(input('Year of pictures\n'))
    folder_name = Path(input('What is the folder name?\n'))
    earliest_date = pd.Timestamp(input('Download media since:\n'))
    latest_date = pd.Timestamp(
            input('Download media until [default is today]:\n'))
    if pd.isnull(latest_date):
        latest_date = pd.Timestamp('now') + pd.Timedelta(days=1)
    if year == Path(''):
        year = Path('2018')
        folder_name = Path('Azores_Madeira')
        earliest_date = pd.Timestamp('2018-09-26')
        latest_date = pd.Timestamp('2018-10-03')
    d = Downloader(earliest_date, latest_date)
    d.copy_files(year / folder_name)


ftp = ftplib.FTP()
ftp.connect(c.FTP_ADDRESS, c.FTP_PORT)
ftp.login()



if __name__ == '__main__':
    run_files()