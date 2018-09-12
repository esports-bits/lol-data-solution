import dropbox
from config.constants import DROPBOX_TOKEN, LEAGUES_DATA_DICT, EXCEL_EXPORT_PATH, SOLOQ_REPORT


class TransferData:
    def __init__(self, access_token):
        self.access_token = access_token

    def upload_file(self, file_from, file_to):
        dbx = dropbox.Dropbox(self.access_token)

        with open(file_from, 'rb') as f:
            dbx.files_upload(f.read(), file_to, mode=dropbox.files.WriteMode.overwrite)


def main(dest_folder):
    access_token = DROPBOX_TOKEN
    transfer_data = TransferData(access_token)

    file_from = '{}'.format(LEAGUES_DATA_DICT[SOLOQ_REPORT][EXCEL_EXPORT_PATH])
    file_to = '/{dest}/soloq_report.xlsx'.format(dest=dest_folder)

    transfer_data.upload_file(file_from, file_to)


if __name__ == '__main__':
    main()
