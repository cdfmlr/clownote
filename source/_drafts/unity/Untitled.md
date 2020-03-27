

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
    transform.Translate(Vector3.forward * Time.deltaTime);
}
```

- `transform.Translate(float x, float y, float z)`：直接传移动坐标；
- `transform.Translate(Vector3.forward)`，传 Vector3 对象，Vector3.forward 是 `new Vector3(0, 0, 1)` 的缩写；
- 

