import dropbox
from config.constants import DROPBOX_TOKEN, LEAGUES_DATA_DICT, EXCEL_EXPORT_PATH, SOLOQ_REPORT, EXPORTS_DIR


class TransferData:
    def __init__(self, access_token):
        self.access_token = access_token

    def upload_file(self, file_from, file_to):
        dbx = dropbox.Dropbox(self.access_token)

        with open(file_from, 'rb') as f:
            dbx.files_upload(f.read(), file_to, mode=dropbox.files.WriteMode.overwrite)


def main(dest_folder, file_name=None):
    access_token = DROPBOX_TOKEN
    transfer_data = TransferData(access_token)

    if file_name is not None:
        file_from = '{}'.format(EXPORTS_DIR + file_name + '.xlsx')
    else:
        file_from = '{}'.format(LEAGUES_DATA_DICT[SOLOQ_REPORT][EXCEL_EXPORT_PATH])
        file_name = 'soloq_dataset'
    file_to = '/{dest}/{file}.xlsx'.format(dest=dest_folder, file=file_name)

    transfer_data.upload_file(file_from, file_to)


if __name__ == '__main__':
    main()
