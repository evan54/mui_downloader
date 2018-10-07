from kivy.app import App
from kivy.uix.gridlayout import GridLayout

from downloader import Downloader
from pathlib import Path
import pandas as pd


class DownloadLayout(GridLayout):
    pass


class InputLayout(GridLayout):

    def run_files(self):
        year = Path(self.ids.year_id.text)
        folder_name = Path(self.ids.folder_id.text)
        earliest_date = pd.Timestamp(self.ids.earliest_date.text)
        latest_date = pd.Timestamp(self.ids.latest_date.text)
        if pd.isnull(latest_date):
            latest_date = pd.Timestamp('now') + pd.Timedelta(days=1)
        if year == Path(''):
            year = Path('2018')
            folder_name = Path('Azores_Madeira')
            earliest_date = pd.Timestamp('2018-09-26')
            latest_date = pd.Timestamp('2018-10-03')
        d = Downloader(earliest_date, latest_date)
        d.copy_files(year / folder_name)


class DownloadApp(App):
    def build(self):
        return InputLayout()


if __name__ == '__main__':
    app = DownloadApp()
    app.run()
