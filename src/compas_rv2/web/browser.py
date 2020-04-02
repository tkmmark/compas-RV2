import os
import subprocess

HERE = os.path.dirname(os.path.realpath(__file__))


def Browser():
    from zipfile import ZipFile

    BIN = os.path.join(HERE, 'electron', 'frontpage.exe')

    if not os.path.exists(BIN):
        print("unziping electron")
        zf = ZipFile(os.path.join(HERE, 'electron.zip'), 'r')
        zf.extractall(os.path.join(HERE, 'electron'))
        zf.close()

    subprocess.Popen('"%s"' % BIN)

if __name__ == '__main__':
    Browser()
