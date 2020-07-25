---
date: 2020-03-26 17:14:49
title: Untitled
---


- 坐标：

| 轴   | Vector3 shorthand | 值        | 说明   | 反方向           |
| ---- | ----------------- | --------- | ------ | ---------------- |
| +x   | Vector3.right     | (1, 0, 0) | 右手边 | left: (-1, 0, 0) |
| +y   | Vector3.up        | (0, 1, 0) | 头顶上 | down: (0, -1, 0) |
| +z   | Vector3.forward   | (0, 0, 1) | 正前方 | back: (0, 0, -1) |

- 一个单位的 Transform Position 可以看成是 1 米。

移动物体：

```csharp
void Update()
{
    // transform.Translate(0, 0, 1);
    // transform.Translate(Vector3.forward);
    transform.Translate(Vector3.forward * Time.deltaTime * 20);
}
```

- `transform.Translate(float x, float y, float z)`：直接传移动坐标；
- `transform.Translate(Vector3.forward)`，传 Vector3 对象，Vector3.forward 是 `new Vector3(0, 0, 1)` 的缩写；

`Vector3.forward * Time.deltaTime` 可以调整速度。在 Update 中的语句会每一帧执行一次，而不同设备上的帧率是不一样的，所以直接用 `transform.Translate(Vector3.forward)` 会产生不同的速度。乘上一个 `Time.deltaTime` （The completion time in seconds since the last frame）即让物体以 `1m/s` 的速度运动，与帧率无关。



