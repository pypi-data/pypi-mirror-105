import subprocess
import tarfile
import zipfile
import os


class Extractor:

    @staticmethod
    def extract(file_path, destination_path):
        if file_path.endswith('.tar'):
            tarfile.open(file_path, 'r').extractall(destination_path)
        elif file_path.endswith('.tgz') or file_path.endswith('.tar.gz'):
            tarfile.open(file_path, 'r:gz').extractall(destination_path)
        elif file_path.endswith('.tar.bz2'):
            tarfile.open(file_path, 'r:bz').extractall(destination_path)
        elif file_path.endswith('.tar.xz'):
            tarfile.open(file_path, 'r:xz').extractall(destination_path)
        elif file_path.endswith('.tar.Z'):
            try:
                subprocess.call(['uncompress'])
            except FileNotFoundError:
                raise Exception('"uncompress" utility must be installed to use this library.')

            stream = subprocess.Popen(f'uncompress {file_path}'.split(' '), stdout=subprocess.PIPE,
                                      stderr=subprocess.STDOUT, universal_newlines=True, )
            stream.wait()
            exitcode = stream.returncode
            if exitcode != 0:
                err = stream.stdout.read()
                raise Exception(f'could not uncompress "{file_path}". error: {err}')

            uncompressed_file = file_path.replace('.tar.Z', '.tar')
            if not os.path.isfile(uncompressed_file):
                raise Exception(f'could not find uncompressed tar file: checked "{uncompressed_file}"')

            tarfile.open(uncompressed_file, 'r').extractall(destination_path)

        elif zipfile.is_zipfile(file_path):
            zipfile.ZipFile(file_path, 'r').extractall(destination_path)
        else:
            raise Exception(f'Unsupported compression type: "{file_path}"')

        return destination_path
