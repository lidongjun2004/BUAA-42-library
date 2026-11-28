"""检查随包数据。文件丢失时，按原始地址下载正式数据。"""
from pathlib import Path
import hashlib
import io
import tarfile
import urllib.request

from data import ROOT, load_rows

URL = 'https://www.cs.cornell.edu/people/pabo/movie-review-data/rt-polaritydata.tar.gz'


def main():
    data_dir = ROOT / 'data' / 'rt-polaritydata'
    expected = ['rt-polarity.neg', 'rt-polarity.pos']
    if not all((data_dir / name).is_file() for name in expected):
        print('正在下载正式数据', URL)
        with urllib.request.urlopen(URL, timeout=60) as response:
            archive = response.read()
        with tarfile.open(fileobj=io.BytesIO(archive), mode='r:gz') as tar:
            members = {m.name: m for m in tar.getmembers() if m.isfile()}
            for name in expected:
                key = 'rt-polaritydata/' + name
                if key not in members:
                    raise ValueError('下载文件缺少' + key)
            data_dir.mkdir(parents=True, exist_ok=True)
            for name in expected:
                member = members['rt-polaritydata/' + name]
                # 仅写入两个已知文件，不使用extractall。
                (data_dir / name).write_bytes(tar.extractfile(member).read())
    load_rows(data_dir)
    for name in expected:
        path = data_dir / name
        print(name, '5331条', 'SHA256', hashlib.sha256(path.read_bytes()).hexdigest())
    print('正式数据检查通过，共10662条。')


if __name__ == '__main__':
    main()
