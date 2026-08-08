# KPU

**[ONGOING]**

KPU is a collection of circuit and computer architecture emulators that I build as experiments and personal projects. More projects will be added over time.

## Installation

Clone the repository:

```bash
git clone https://github.com/Kumail-exp/KPU.git
cd KPU
```

Install the required Python dependencies:

```bash
pip install -r requirements.txt
```

## VS Code Extension

KPU includes a small VS Code extension for **KPU Assembly** syntax highlighting.

### Requirements

* VS Code
* Node.js
* npm

### Installation

Enter the extension directory:

```bash
cd kpu-vscode
```

Install `vsce`:

```bash
npm install -g @vscode/vsce
```

Package the extension:

```bash
vsce package --allow-missing-repository
```

This will create:

```text
kpu-assembly-0.0.1.vsix
```

Install the extension:

```bash
code --install-extension kpu-assembly-0.0.1.vsix
```

Restart VS Code, then open any `.asm` file. VS Code should automatically recognize it as **KPU Assembly** and provide syntax highlighting.

### Manual Installation

You can also install the `.vsix` file directly through VS Code:

1. Open **Extensions** (`Ctrl+Shift+X`)
2. Click the `...` menu
3. Select **Install from VSIX...**
4. Select `kpu-assembly-0.0.1.vsix`
5. Reload VS Code

## Project-Specific Documentation

For installation instructions, usage, and other details, check the README of each individual project.

## Current Projects

* [NAND-8](NAND-8/readme.md)
* [KPU16](KPU16/readme.md)
