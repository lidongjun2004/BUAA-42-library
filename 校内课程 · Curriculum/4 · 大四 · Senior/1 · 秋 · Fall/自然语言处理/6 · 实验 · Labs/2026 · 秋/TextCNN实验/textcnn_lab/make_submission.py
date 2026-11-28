"""在实验根目录生成提交包，保留代码和结果，省去权重文件。"""
import argparse
from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parent


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--name', default='submission', help='例如20260001_张三')
    args = parser.parse_args()
    if not args.name.strip() or any(char in args.name for char in '/\\:*?"<>|') or args.name in ('.', '..'):
        parser.error('--name应填写学号_姓名，不要包含路径符号')
    required = ['TextCNN.ipynb', 'data.py', 'model.py', 'train.py', 'check_tasks.py',
                'prepare_data.py', 'make_submission.py', 'my_reviews.txt',
                'requirements.txt', 'DATA_SOURCES.md', '实验报告.docx']
    for run in ['baseline', 'compare']:
        for filename in ['metrics.json', 'history.csv', 'predictions.csv', 'validation_predictions.csv']:
            required.append(f'results/{run}/{filename}')
    missing = [name for name in required if not (ROOT / name).is_file()]
    if missing:
        raise FileNotFoundError('提交材料缺少以下文件\n' + '\n'.join(missing))
    filename = 'submission.zip' if args.name == 'submission' else f'{args.name}_TextCNN.zip'
    path = ROOT / filename
    with zipfile.ZipFile(path, 'w', compression=zipfile.ZIP_DEFLATED) as archive:
        for name in required:
            archive.write(ROOT / name, name)
    print('已生成', filename, '。请下载并按课堂要求提交。')


if __name__ == '__main__':
    main()
