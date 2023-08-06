import shutil
import re
import os
from kpl_helper.base import get_config, _APIBase
from requests_toolbelt import MultipartEncoder, MultipartEncoderMonitor
import uuid
import logging

HAN_SCRIPT_PAT = re.compile(
    r'[\u4E00-\u9FEF\u3400-\u4DB5\u20000-\u2A6D6\u2A700-\u2B734'
    r'\u2B740-\u2B81D\u2D820-\u2CEA1\u2CEB0-\u2EBE0]'
)
MB = 1024 * 1024


def is_archive_file(path):
    if os.path.isdir(path):
        return False
    if path.endswith(".tar") or path.endswith(".tar.gz") or path.endswith(".zip"):
        return True
    return False


def assert_symbol_link(path):
    path = os.path.abspath(path)
    if os.path.islink(path):
        raise Exception("[kpl-helper]: `{}` is symbol link. cannot make archive".format(path))


class _UploadProgress:
    def __init__(self, total, bar_size=50):
        if total < 1024:
            self.unit_divisor = 1
            self.unit = "B"
        elif total < MB:
            self.unit_divisor = 1024
            self.unit = "KB"
        else:
            self.unit_divisor = MB
            self.unit = "MB"
        self.total = int(total / self.unit_divisor)
        self.bar_size = bar_size

    def update(self, current):
        current = int(current / self.unit_divisor)
        progress = int(current * self.bar_size / self.total)
        completed = str(int(current * 100 / self.total)) + '%'
        print('Progress: [{} {}{}] {}/{}{}'.format(chr(9608) * progress, completed,
                                                   '.' * (self.bar_size - progress),
                                                   current, self.total, self.unit), end='\r', flush=True)

    def close(self):
        print("\n")


class Uploader(_APIBase):
    @staticmethod
    def _make_archive(root_dir, base_dir):
        tar_path = os.path.join("/tmp", uuid.uuid4().hex)
        shutil.make_archive(tar_path, "tar",
                            root_dir=root_dir,
                            base_dir=base_dir)
        return tar_path + ".tar"

    def _upload(self, route, name, desc, path, make_archive=False, size_limit=None):
        path = os.path.abspath(path)
        if os.path.islink(path):
            raise Exception("[kpl-helper]: `{}` is symbol link. cannot make archive".format(path))
        if not get_config().get_inner():
            return
        upload_file = path
        if make_archive:
            root_dir = os.path.abspath(os.path.join(path, ".."))
            upload_file = self._make_archive(root_dir, os.path.basename(path))

        file_size = os.path.getsize(upload_file)
        if size_limit is not None and file_size > size_limit:
            raise Exception("[kpl-helper]: file size `{}MB` exceeds limit of 50MB".format(size_limit / MB))
        bar = _UploadProgress(file_size)

        def upload_callback(m):
            bar.update(m.bytes_read)

        with open(upload_file, "rb") as fi:
            encoder = MultipartEncoder(
                fields={'name': name, 'description': desc,
                        'file': (os.path.basename(upload_file), fi, 'text/plain')}
            )
            monitor = MultipartEncoderMonitor(encoder, upload_callback)
            self.post(route, data=monitor, headers={'Content-Type': monitor.content_type})
        bar.close()
        if make_archive:
            os.remove(upload_file)

    def upload_dataset(self, name, desc, path):
        # 如果是单个文件，且是.tar/.tar.gz/.zip文件，则直接上传
        # 如果是单个文件，且非.tar/.tar.gz/.zip文件，则需要对文件打包上传
        # 如果是文件夹，则需要对目录打包上传
        self._upload("/dataset/upload", name, desc, path, not is_archive_file(path))

    def upload_dataset_fs(self, name, desc, path):
        # 如果是单个文件，且是.tar/.tar.gz/.zip文件，则直接上传
        # 如果是单个文件，且非.tar/.tar.gz/.zip文件，则需要对文件打包上传
        # 如果是文件夹，则需要对目录打包上传
        self._upload("/dataset_fs/upload", name, desc, path, not is_archive_file(path))

    def upload_model(self, name, desc, path):
        # 模型如果是单个文件则不需要打包，否则需要打包成.tar文件再上传
        self._upload("/model/upload", name, desc, path, os.path.isdir(path))

    def upload_algorithm(self, name, desc, path):
        self._upload("/algorithm/upload", name, desc, path, not is_archive_file(path), 50 * MB)


def save_dataset(path, name, description, as_serialized=False):
    try:
        uploader = Uploader()
        if as_serialized:
            uploader.upload_dataset(name, description, path)
        else:
            uploader.upload_dataset_fs(name, description, path)
    except Exception as e:
        logging.exception(e)


def save_model(path, name, description):
    try:
        uploader = Uploader()
        uploader.upload_model(name, description, path)
    except Exception as e:
        logging.exception(e)


def save_algorithm(path, name, description):
    try:
        uploader = Uploader()
        uploader.upload_algorithm(name, description, path)
    except Exception as e:
        logging.exception(e)
