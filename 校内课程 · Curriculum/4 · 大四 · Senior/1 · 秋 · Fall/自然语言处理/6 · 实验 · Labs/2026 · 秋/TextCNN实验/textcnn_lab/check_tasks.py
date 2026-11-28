"""按任务检查代码。示例数据仅用于检查，与正式训练数据分开。"""
import argparse
import numpy as np
from data import encode, tokenize


def check_encode():
    vocab = {'<PAD>': 0, '<UNK>': 1, 'good': 2, 'film': 3, 'very': 4}
    assert tokenize('Good FILM!') == ['good', 'film']
    result = encode('Good film!', vocab, 5)
    np.testing.assert_array_equal(result, [2, 3, 0, 0, 0])
    assert result.dtype == np.int32 and result.shape == (5,)
    np.testing.assert_array_equal(encode('A good film', vocab, 5), [1, 2, 3, 0, 0])
    np.testing.assert_array_equal(encode('very very good film', vocab, 3), [4, 4, 2])
    np.testing.assert_array_equal(encode('', vocab, 3), [0, 0, 0])
    print('任务1通过。已检查小写、标点、未知词、补齐和截断。')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--task', type=int, choices=[1, 2, 3, 4])
    parser.add_argument('--device', choices=['CPU', 'GPU', 'Ascend'], default='CPU')
    args = parser.parse_args()
    tasks = [args.task] if args.task else [1, 2, 3, 4]
    if 1 in tasks:
        check_encode()
    if tasks == [1]:
        return
    import mindspore as ms
    from mindspore import nn, Tensor
    from model import TextCNN
    from train import train_step, predict, classification_metrics
    ms.set_context(mode=ms.PYNATIVE_MODE, device_target=args.device)
    ms.set_seed(42)
    np.random.seed(42)
    net = TextCNN(12, 10)
    x = Tensor(np.arange(20, dtype=np.int32).reshape(2, 10) % 12)
    labels = Tensor(np.asarray([0, 1], dtype=np.int32))
    if 2 in tasks:
        for kernels in [(3, 4, 5), (2, 3, 4)]:
            candidate = TextCNN(12, 10, kernels=kernels)
            candidate.set_train(False)
            logits = candidate(x).asnumpy()
            assert logits.shape == (2, 2), f'输出应为(2,2)，实际{logits.shape}'
            assert np.isfinite(logits).all(), '输出含NaN或无穷大'
        print('任务2通过。两组卷积核的输出形状均为[batch,2]。')
    if 3 in tasks:
        net.set_train(True)
        loss_fn = nn.SoftmaxCrossEntropyWithLogits(sparse=True, reduction='mean')
        optimizer = nn.Adam(net.trainable_params(), learning_rate=1e-3)
        def forward(data, target):
            return loss_fn(net(data), target)
        grad_fn = ms.value_and_grad(forward, None, optimizer.parameters)
        before = [p.asnumpy().copy() for p in net.trainable_params()]
        loss = train_step(x, labels, grad_fn, optimizer)
        assert loss.shape == () and np.isfinite(loss.asnumpy()), '应返回有限的标量损失'
        changed = any(not np.array_equal(old, p.asnumpy())
                      for old, p in zip(before, net.trainable_params()))
        assert changed, '参数没有更新，请检查是否调用optimizer(grads)'
        print('任务3通过。一次训练后至少有一个参数发生变化。')
    if 4 in tasks:
        class FixedClassifier(nn.Cell):
            def __init__(self, logits):
                super().__init__()
                self.logits = Tensor(np.asarray([logits], dtype=np.float32))
            def construct(self, data):
                return self.logits
        vocab = {'<PAD>': 0, '<UNK>': 1, 'good': 2}
        positive = FixedClassifier([0.1, 0.9])
        negative = FixedClassifier([0.9, 0.1])
        assert predict('A good film!', positive, vocab, 5) == 1
        assert predict('Unknown words', negative, vocab, 5) == 0
        assert not positive.training, '预测前需要关闭训练模式'
        scores = classification_metrics([1, 1, 0, 0], [1, 0, 1, 0])
        assert scores['accuracy'] == scores['precision'] == scores['recall'] == scores['f1'] == 0.5
        print('任务4通过。已检查两类标签和预测模式。')


if __name__ == '__main__':
    main()
