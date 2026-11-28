"""训练、验证和预测，从实验根目录运行。"""
import argparse
import csv
import json
from pathlib import Path
import time

import mindspore as ms
from mindspore import nn, Tensor
import numpy as np

from data import ROOT, SEED, encode, prepare_data
from model import TextCNN

GIVEN_REVIEWS = [
    'This is a film well worth seeing .',
    'On its own , it is not very interesting .',
]


def train_step(data, labels, grad_fn, optimizer):
    """grad_fn已包装损失函数。返回本批损失，同时更新一次参数。"""
    # TODO 3  通过grad_fn求损失和梯度，更新参数并返回损失。
    raise NotImplementedError("请完成任务3")


def predict(text, net, vocab, word_len):
    """返回0或1，0表示负面，1表示正面。"""
    # TODO 4  关闭训练模式，编码一句文本，计算输出并返回类别0或1。
    raise NotImplementedError("请完成任务4")


def classification_metrics(labels, predictions):
    labels = np.asarray(labels)
    predictions = np.asarray(predictions)
    tp = int(np.sum((labels == 1) & (predictions == 1)))
    fp = int(np.sum((labels == 0) & (predictions == 1)))
    fn = int(np.sum((labels == 1) & (predictions == 0)))
    tn = int(np.sum((labels == 0) & (predictions == 0)))
    precision = tp / (tp + fp) if tp + fp else 0.0
    recall = tp / (tp + fn) if tp + fn else 0.0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
    return {'accuracy': (tp + tn) / len(labels), 'precision': precision,
            'recall': recall, 'f1': f1, 'tp': tp, 'fp': fp, 'fn': fn, 'tn': tn}


def evaluate(net, x, y, loss_fn, batch_size=64):
    net.set_train(False)
    predictions, total_loss = [], 0.0
    for start in range(0, len(y), batch_size):
        end = min(start + batch_size, len(y))
        logits = net(Tensor(x[start:end], ms.int32))
        loss = loss_fn(logits, Tensor(y[start:end], ms.int32))
        total_loss += float(loss.asnumpy()) * (end - start)
        predictions.extend(np.argmax(logits.asnumpy(), axis=1).tolist())
    metrics = classification_metrics(y, predictions)
    metrics['loss'] = total_loss / len(y)
    return metrics, predictions


def write_csv(path, rows, columns):
    with Path(path).open('w', encoding='utf-8-sig', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)


def read_my_reviews():
    path = ROOT / 'my_reviews.txt'
    reviews = [s.strip() for s in path.read_text(encoding='utf-8').splitlines()
               if s.strip() and not s.lstrip().startswith('#')]
    if len(reviews) != 2:
        raise ValueError('请在my_reviews.txt中写两句自拟英文影评，每行一句，再开始训练。')
    return reviews


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--device', choices=['CPU', 'GPU', 'Ascend'], default='CPU')
    parser.add_argument('--run', choices=['baseline', 'compare'], default='baseline')
    parser.add_argument('--epochs', type=int, default=8)
    parser.add_argument('--predict-only', action='store_true')
    args = parser.parse_args()
    if args.epochs < 1:
        parser.error('--epochs必须至少为1')
    my_reviews = read_my_reviews()
    ms.set_context(mode=ms.PYNATIVE_MODE, device_target=args.device)
    ms.set_seed(SEED)
    np.random.seed(SEED)
    train, valid, vocab, info, valid_rows = prepare_data()
    train_x, train_y = train
    valid_x, valid_y = valid
    kernels = (3, 4, 5) if args.run == 'baseline' else (2, 3, 4)
    net = TextCNN(len(vocab), info['word_len'], kernels=kernels)
    loss_fn = nn.SoftmaxCrossEntropyWithLogits(sparse=True, reduction='mean')
    optimizer = nn.Adam(net.trainable_params(), learning_rate=1e-3, weight_decay=3e-5)
    out = ROOT / 'results' / args.run
    out.mkdir(parents=True, exist_ok=True)
    checkpoint = out / 'last.ckpt'
    print('运行', args.run, '设备', args.device, 'MindSpore', ms.__version__)
    print('数据', json.dumps(info, ensure_ascii=False))

    def forward(x, labels):
        return loss_fn(net(x), labels)

    grad_fn = ms.value_and_grad(forward, None, optimizer.parameters)
    if args.predict_only:
        if not checkpoint.is_file():
            raise FileNotFoundError('还没有last.ckpt，请先完成该组训练。')
        ms.load_param_into_net(net, ms.load_checkpoint(str(checkpoint)))
    else:
        # 新训练覆盖本组旧结果。
        for filename in ['metrics.json', 'history.csv', 'predictions.csv',
                         'validation_predictions.csv', 'last.ckpt']:
            (out / filename).unlink(missing_ok=True)
        history = []
        batch_size = 16
        rng = np.random.default_rng(SEED)
        for epoch in range(1, args.epochs + 1):
            started = time.perf_counter()
            net.set_train(True)
            order = rng.permutation(len(train_y))
            total_loss = 0.0
            for start in range(0, len(order), batch_size):
                indices = order[start:start + batch_size]
                batch_loss = train_step(Tensor(train_x[indices], ms.int32),
                                        Tensor(train_y[indices], ms.int32), grad_fn, optimizer)
                total_loss += float(batch_loss.asnumpy()) * len(indices)
            metrics, predictions = evaluate(net, valid_x, valid_y, loss_fn)
            record = {'epoch': epoch, 'train_loss': total_loss / len(train_y),
                      'valid_loss': metrics['loss'], 'accuracy': metrics['accuracy'],
                      'precision': metrics['precision'], 'recall': metrics['recall'],
                      'f1': metrics['f1'], 'seconds': time.perf_counter() - started}
            history.append(record)
            write_csv(out / 'history.csv', history, list(record))
            print(f"第{epoch}/{args.epochs}轮  训练损失{record['train_loss']:.4f}  "
                  f"验证准确率{record['accuracy']:.4f}  F1={record['f1']:.4f}  "
                  f"用时{record['seconds']:.1f}秒", flush=True)
        # 统一报告最后一轮的结果，权重也来自同一轮。
        ms.save_checkpoint(net, str(checkpoint))
        final_metrics = {**metrics, **info, 'run': args.run, 'kernels': list(kernels),
                         'embedding_dim': 40, 'channels_per_kernel': 96,
                         'dropout': 0.5, 'batch_size': batch_size, 'learning_rate': 1e-3,
                         'weight_decay': 3e-5, 'epochs': args.epochs, 'checkpoint': 'last.ckpt',
                         'device': args.device, 'mindspore_version': ms.__version__}
        (out / 'metrics.json').write_text(json.dumps(final_metrics, ensure_ascii=False, indent=2), encoding='utf-8')
        write_csv(out / 'validation_predictions.csv',
                  [{'text': text, 'label': label, 'prediction': pred}
                   for (text, label), pred in zip(valid_rows, predictions)],
                  ['text', 'label', 'prediction'])
    reviews = GIVEN_REVIEWS + my_reviews
    prediction_rows = [{'source': 'given' if i < 2 else 'mine', 'text': text,
                        'prediction': predict(text, net, vocab, info['word_len'])}
                       for i, text in enumerate(reviews)]
    write_csv(out / 'predictions.csv', prediction_rows, ['source', 'text', 'prediction'])
    for row in prediction_rows:
        print(row['text'], 'Positive' if row['prediction'] == 1 else 'Negative')
    print('结果已保存到', out)


if __name__ == '__main__':
    main()
