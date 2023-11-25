# simple_filler

- ゼロ埋め以外のなにか特定のパターンで埋めたいとき用のディスク上書きスクリプト
- 本当は/dev/zeroみたいなキャラクターデバイスを作ってddしたいが、これでもそんなに速度悪くない(ddのブロックサイズ次第)ので、これで良いかという感じ
- パーティションやファイルを対象に上書きは×

## 使用例
```./simple_filler.py /dev/loop0 --blocksize=$((1024*1024)) --message='This is a test message'```
