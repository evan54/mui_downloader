import os
import pandas as pd
from pathlib import Path
import subprocess
import bs4
import ftplib

import config as c


class Downloader:

    def __init__(self, earliest_date, latest_date):
        self.earliest_date = earliest_date
        self.latest_date = latest_date
        self.address = f'ftp://{c.FTP_ADDRESS}:{c.FTP_PORT}'

        ftp = ftplib.FTP()
        ftp.connect(c.FTP_ADDRESS, c.FTP_PORT)
        ftp.login()
        self.ftp = ftp

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
            self.ftp.cwd(cwd)
            self.ftp.delete(name)


def run_files():
    year = Path(input('Year of pictures [default is current year]\n'))
    if year == Path(''):
        year = Path(pd.Timestamp('now').strftime('%Y'))

    folder_name = Path(input('What is the folder name? [default is temp]\n'))
    if folder_name == Path(''):
        folder_name = Path('temp')

    latest_date = pd.Timestamp(
            input('Download media until [default is today]:\n'))
    if pd.isnull(latest_date):
        latest_date = pd.Timestamp('now') + pd.Timedelta(days=1)

    earliest_date = pd.Timestamp(input('Download media since:\n'))

    d = Downloader(earliest_date, latest_date)
    d.copy_files(year / folder_name)


if __name__ == '__main__':
    run_files()
