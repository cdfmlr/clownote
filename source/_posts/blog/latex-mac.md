---
date: 2022-03-10 18:30:26.739962
title: 一种macOS系统下的LaTeX最小安装方法
---
# 一种 macOS 系统下的 $\LaTeX$ 最小安装方法

BasicTeX + CTeX + VS Code (LaTeX Workshop)

## TL;DR

```sh
brew install basictex

# VS Code 装 LaTeX Workshop

# ctex
sudo tlmgr update --self
sudo tlmgr update texlive-scripts
sudo tlmgr update --all
sudo tlmgr install ctex

# LaTeX Workshop 插件依赖
# latexmk
sudo tlmgr install latexmk
echo '$pdflatex = "xelatex %O %S";' > ~/.latexmkrc
# latexindent
sudo tlmgr install latexindent
sudo cpan Log::Log4perl
sudo cpan Log::Dispatch
sudo cpan YAML::Tiny
sudo cpan File::HomeDir
sudo cpan Unicode::GCString
```

## Full story

0. 先决条件：
   - Homebrew
   - Visual Studio Code


1. 装 basictex：

```sh
brew install basictex
```

2. 装 ctex：
   参考 [tex.stackexchange: Cannot install ctex via tlmgr: "Unknown option: status-file" when running fmtutil-sys](https://tex.stackexchange.com/questions/598380/cannot-install-ctex-via-tlmgr-unknown-option-status-file-when-running-fmtuti)

```sh
sudo tlmgr update --self
sudo tlmgr update texlive-scripts
sudo tlmgr update --all
sudo tlmgr install ctex
```

3. 装 VS Code 插件：
   See [James-Yu](https://github.com/James-Yu)/**[LaTeX-Workshop](https://github.com/James-Yu/LaTeX-Workshop)**

4. 装 latexmk，配置 pdfTex => XeLaTeX
   参考 [tex.stackexchange: How to make LaTeXmk work with XeLaTeX and biber](https://tex.stackexchange.com/questions/27450/how-to-make-latexmk-work-with-xelatex-and-biber)

```sh
# latexmk
sudo tlmgr install latexmk
echo '$pdflatex = "xelatex %O %S";' > ~/.latexmkrc
```

5. 装缩进处理程序：
   参考 [James-Yu/LaTeX-Workshop #376 Formatting failed error](https://github.com/James-Yu/LaTeX-Workshop/issues/376)

```sh
# latexindent: https://github.com/James-Yu/LaTeX-Workshop/issues/376
sudo tlmgr install latexindent
sudo cpan Log::Log4perl
sudo cpan Log::Dispatch
sudo cpan YAML::Tiny
sudo cpan File::HomeDir
sudo cpan Unicode::GCString
```