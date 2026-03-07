# Gradle 命令内存占用分析

在 macOS 上分析 Gradle 构建及其所有子进程的内存消耗。使用系统 `footprint` 命令测量物理内存；输出可交互的 HTML 图表。

## 环境要求

- macOS（依赖 `footprint` 和 `vm_stat`）
- Python 3.9+
- `pip install plotly`（必需；若未安装，脚本会退出并提示安装命令）
- 项目目录下需有 `./gradlew`

## 安装

```bash
pip install -r requirements.txt
```

## 使用

在任意目录执行，需指定项目目录和完整 Gradle 命令：

```bash
python gradle_mem_analyze.py -d /path/to/gradle/project -- ./gradlew :composeApp:linkReleaseSharedOhosArm64 --rerun-tasks
```

### 选项

- `-d`, `--dir`：项目目录（必填），目录下必须有 `gradlew`
- `-i`, `--interval`：轮询间隔（秒），默认 1

### 示例

```bash
python gradle_mem_analyze.py -d ~/git/sample/ovCompose-sample -i 2 -- ./gradlew :composeApp:linkReleaseSharedOhosArm64 --rerun-tasks
```

构建输出写入输出目录下的 `gradle_output.log`。可在另一终端执行 `tail -f mem_analyze_output/<run>/gradle_output.log` 实时查看进度。

## 输出

每次运行在 `mem_analyze_output/` 下生成带时间戳的文件夹（如 `2026-03-07_16-34-53/`）：

1. **可交互 HTML 图表**（在浏览器中打开，支持缩放、悬停、平移）：
   - **phys_mem_per_process.html**：每个进程一条曲线，X=时间，Y=物理内存（MB）。曲线从该子进程首次出现时开始。
   - **total_tree_over_time.html**：树总内存（MB）与系统空闲内存减少量（MB）随时间变化。两者均随构建占用内存而增加。

2. **footprint/**：每次采样的 `footprint -t` 原始输出（如 `sample_0000_tree.txt` 等）

3. **gradle_output.log**：完整 Gradle 构建输出

4. **控制台**：峰值内存表（按进程及整棵树）

## 工作原理

1. 检查 plotly 是否已安装，未安装则退出并给出安装说明
2. 执行 `./gradlew --stop`： 确保 daemon 都是这次的 ./gradlew 命令拉起，这样 footprint 才能看到所有的子进程
3. 启动 Gradle 命令，stdout/stderr 重定向到 `gradle_output.log`
4. 每隔 N 秒轮询一次 `footprint -t -p root` 和 `vm_stat`
5. 从 footprint 输出解析各进程数据及 Summary Footprint
6. 构建结束后生成 Plotly 交互式 HTML 图表并打印峰值表
