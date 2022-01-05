---
date: 2021-12-31 15:38:42.780043
title: 将 Homebrew 安装的 Python 加入 pyenv 版本管理
---
# 将 Homebrew 安装的 Python 加入 pyenv 版本管理

1. 给版本软链接到 pyenv

   ```sh
   cd ~/.pyenv/versions
   ln -sfv "$(brew --prefix python@3.9)" 3.9
   ```

2. include（意义不明，并且会报错）

   ```sh
   cd "$(brew --prefix python@3.9)"
   ln -sfv Frameworks/Python.framework/Versions/3.9/include/python3.9 include
    include -> Frameworks/Python.framework/Versions/3.9/include/python3.9
   ```

3. 继续给执行文件软链接

   ```sh
   cd "$(brew --prefix python@3.9)/bin"
   ln -sfv idle3 idle
   ln -sfv pip3 pip 
   ln -sfv python3 python
   ln -sfv wheel3 wheel
   ```

4. pyenv 重新索引

   ```sh
   pyenv rehash
   pyenv versions
   ```

   可以看到已经有 homebrew 装的版本了。可以用了： ` pyenv global 3.9`

⚠️ 如果遇到 homebrew 的 Python 把系统的占了（pyenv 显示在用系统自带的 system，但实际上 `which python3` 是 homebrew 的版本，同时 `pyenv global` 无法实际上切换版本），则需要：

```sh
brew unlink python@3.9
pyenv rehash
```

然后你再尝试 `pyenv global` 就可以真的改动全局 Python 版本了。

## 参考

[Stackoverflow 30499795: How can I make homebrew's python and pyenv live together?](https://stackoverflow.com/questions/30499795/how-can-i-make-homebrews-python-and-pyenv-live-together)


[César Román: how-to-add-python-installed-via-homebrew-to-pyenv-versions](https://thecesrom.dev/2021/06/28/how-to-add-python-installed-via-homebrew-to-pyenv-versions/)

