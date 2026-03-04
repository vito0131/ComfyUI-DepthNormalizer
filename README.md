# ComfyUI-DepthNormalizer

A ComfyUI custom node for normalizing depth maps to a specific range (0–190 by default).

## 简介

ComfyUI-DepthNormalizer 提供了一个自定义节点，用于将深度图按 0–255 灰阶域进行归一化和拉伸，使输出稳定在 0–190（可配置）。

**核心功能：**
- 在 8-bit 域（0-255）中手动设置最小/最大值进行重映射
- 支持将输出最大值映射到目标值（默认 190）
- 可选减去最小值，强制黑色为 0
- 自动处理 ComfyUI IMAGE 格式（0-1 float）与 8-bit 域的转换

## 安装方式

### 方式一：通过 ComfyUI Manager 安装（推荐）

1. 打开 ComfyUI，点击 **Manager** 按钮
2. 选择 **Install Custom Nodes**
3. 搜索 "DepthNormalizer" 或输入仓库地址
4. 点击安装并重启 ComfyUI

### 方式二：手动安装

```bash
# 进入 ComfyUI 的 custom_nodes 目录
cd /path/to/ComfyUI/custom_nodes

# 克隆仓库
git clone https://github.com/vito0131/ComfyUI-DepthNormalizer.git

# 重启 ComfyUI
```

## 节点说明

### Depth Range → 0–190 (Manual)

将深度图按指定的 8-bit 范围进行归一化，输出到目标范围。

#### 输入参数

| 参数名 | 类型 | 默认值 | 范围 | 说明 |
|--------|------|--------|------|------|
| `image` | IMAGE | - | - | 输入深度图（ComfyUI IMAGE 格式，0-1 float） |
| `min_8bit` | INT | 0 | 0-255 | 输入深度图在 8-bit 域的最小值 |
| `max_8bit` | INT | 190 | 0-255 | 输入深度图在 8-bit 域的最大值 |
| `target_max_8bit` | INT | 190 | 1-255 | 输出深度图在 8-bit 域的目标最大值 |
| `subtract_min` | BOOLEAN | True | - | 是否先减去最小值，使黑色强制为 0 |
| `clamp_to_target` | BOOLEAN | True | - | 是否将输出限制在目标范围内 |

#### 输出

| 输出名 | 类型 | 说明 |
|--------|------|------|
| `image` | IMAGE | 归一化后的深度图（ComfyUI IMAGE 格式，0-1 float） |

#### 处理逻辑

1. 将输入从 0-1 float 转换为 0-255 域：`x255 = image * 255.0`
2. 根据 `subtract_min` 参数选择重映射方式：
   - 如果为 True：`y255 = (x255 - min) * (target / (max - min))`
   - 如果为 False：`y255 = x255 * (target / max)`
3. 根据 `clamp_to_target` 进行裁剪：
   - 如果为 True：限制在 `[0, target]`
   - 如果为 False：限制在 `[0, 255]`
4. 转换回 0-1 float：`output = y255 / 255.0`

## 使用示例

### 示例：将深度范围 1-117 拉伸到 0-190

假设你有一个深度图，其有效深度值在 8-bit 域的范围是 1 到 117，你希望将其拉伸到 0-190 范围：

| 参数 | 值 |
|------|-----|
| `min_8bit` | 1 |
| `max_8bit` | 117 |
| `target_max_8bit` | 190 |
| `subtract_min` | ✅ True |
| `clamp_to_target` | ✅ True |

**效果：**
- 输入值 1 将映射到 0
- 输入值 117 将映射到 190
- 中间值线性插值

## 分类

在 ComfyUI 节点树中位于：**Depth/Normalize**

## 许可证

MIT License
