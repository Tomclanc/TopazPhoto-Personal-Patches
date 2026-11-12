# Topaz Photo Personal Patches

仅供个人使用，根据个人审美修改。

记录 2026-11-12 对本机 Topaz Photo 1.8.1 的外观调整：Windows Mica、原生圆角，以及跟随系统深色 / 浅色的外观。非官方项目，与 Topaz Labs 无关联。

## 修改内容

- 主窗口启用 Mica，标题栏和欢迎页背景显示系统材质。
- 使用 Windows 原生圆角，最大化时由系统显示直角。
- 保留程序原有的 `auto` 主题设置，通过 `WonderStyle.darkMode` 同步原生材质的深浅色。
- 图片预览和编辑面板保留原有颜色。
- 仅重新加载根 `main.qml`，保留其他组件原有的汉化预编译资源，并恢复根界面的中文提示。
- Qt 绘图环境变量只对本次子进程生效。

## 文件

| 文件 | 用途 |
| --- | --- |
| `src/MicaTheme.qml` | Mica 和深浅色同步、欢迎页背景处理 |
| `src/MicaHost.cs` | 启动辅助程序、Qt 绘图参数、原生圆角 |
| `tools/patch_exe.py` | 从指定版本的本地原始 EXE 重建今天的最终补丁 |
| `build.ps1` | 编译启动辅助程序 |
| `manifest.json` | 本次最终文件的 SHA-256 和验证记录 |

仓库只保存本次外观修改源码、脚本和校验记录，不包含 Topaz 主程序、模型、便携包、照片、注册表或账号数据。Topaz 及相关第三方组件的权利归各自权利人所有；请自行取得合法软件授权。本项目未授予第三方软件的使用或分发权利。

## 适用范围

Windows 11、具备 Mica 支持的桌面环境，以及本次记录的 Topaz Photo 1.8.1 本地版本。

补丁严格校验原始 EXE 的 SHA-256：

```
e559d9c867d7ad2c92007aa72c695ee1659ccabaefc06465cc76d8baa82fa61d
```

这是本地备份的校验值，不代表官方安装包校验值。其他版本或不同构建会被拒绝；不要直接套用。

## 本地重建

需要 Python 3 和 Windows .NET Framework C# 编译器。先关闭 Topaz Photo 和便携启动器，备份主程序及启动 INI。

1. 在仓库目录运行 `powershell -ExecutionPolicy Bypass -File .\build.ps1`。
2. 使用未修改的备份 EXE 生成新文件，输出路径必须不存在：

   ```powershell
   python .\tools\patch_exe.py 'D:\Downloads\TopazPhoto\MicaBackup-20261112\Topaz Photo.exe' '.\build\Topaz Photo.exe'
   ```

3. 将生成的 `build/Topaz Photo.exe`、`build/TopazPhotoMicaHost.exe` 和 `src/MicaTheme.qml` 放入本地 Topaz 的 `App` 目录；替换前保留原始文件备份。
4. 对于本次使用的便携启动器，只把 `TopazPhotoPortable.ini` 的 `[GENERAL]` 中 `application` 改为 `App\TopazPhotoMicaHost.exe`，保留其余配置。继续通过原来的便携启动器运行。
5. 程序配色设置保留为 `auto`。独立主题文件必须与主程序位于同一目录。

脚本同时校验输出是否等于今天的最终 EXE；哈希不符时不会写出文件。更新主程序会覆盖补丁。

## 验证记录

今天的现场记录：原生窗口属性 `Backdrop=2`、`Corners=2`、`Dark=0`，主题模块已加载，中文界面已确认正常，没有发现新增的 QML TypeError / ReferenceError。

跟随系统使用原程序已有的主题监听器和属性绑定；尚未实际切换 Windows 深浅色往返验证。未做 AI 模型处理和图像导出回归测试。

恢复时关闭程序，将备份 EXE 和原便携启动 INI 复制回原位置即可。新增的主题与辅助程序可保留，恢复入口后不会再加载。
