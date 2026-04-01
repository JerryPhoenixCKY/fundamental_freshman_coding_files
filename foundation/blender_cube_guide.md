# Blender立方体创建指南

## 问题说明
您遇到的错误是因为`bpy`模块只能在Blender内部使用，不能通过外部Python环境运行。

## 正确使用方法

### 方法1：在Blender内部运行脚本
1. **打开Blender**
2. **切换到Scripting工作区**：
   - 点击顶部菜单栏的"Scripting"选项卡
   - 或者按 `Shift+F11` 打开文本编辑器

3. **加载脚本**：
   - 在文本编辑器中点击"Open"按钮
   - 选择文件：`create_cube_80x20x100.py`

4. **运行脚本**：
   - 点击"Run Script"按钮
   - 或按 `Alt+P`

### 方法2：使用Blender命令行运行
```bash
# 在命令行中运行（需要先安装Blender）
blender --background --python "d:/primary coding files/create_cube_80x20x100.py"
```

### 方法3：手动创建立方体
如果您不想使用脚本，可以手动创建：

1. **打开Blender**
2. **删除默认立方体**（按`A`全选，然后按`Delete`）
3. **添加新立方体**：
   - 按 `Shift+A` → Mesh → Cube
4. **设置尺寸**：
   - 按 `N` 打开侧边栏
   - 在"Item"选项卡中设置尺寸：
     - X: 80
     - Y: 20  
     - Z: 100

## 注意事项
- `bpy`模块只能在Blender内部使用
- 确保Blender已正确安装
- 脚本需要在Blender的Python环境中运行

## 验证安装
在Blender的Python控制台中运行：
```python
import bpy
print("Blender Python环境正常")
```