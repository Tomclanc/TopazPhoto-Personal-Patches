from pathlib import Path
import json,re,zlib,hashlib
import argparse
parser=argparse.ArgumentParser(description="Apply the personal Mica root-QML patch to the exact supported Topaz Photo binary.")
parser.add_argument("input", type=Path, help="Original Topaz Photo.exe (SHA-256 must match)")
parser.add_argument("output", type=Path, help="New patched executable; must not already exist")
args=parser.parse_args()
original=args.input.read_bytes()
expected="e559d9c867d7ad2c92007aa72c695ee1659ccabaefc06465cc76d8baa82fa61d"
if hashlib.sha256(original).hexdigest()!=expected:
    parser.error("Unsupported input SHA-256; no output was written. This patch only supports the recorded local 1.8.1 build.")
if args.output.exists():
    parser.error("Output already exists; choose a new path.")
b=bytearray(original)
s=zlib.decompress(b[593443304:593504000]).decode()
# Restore the existing localized captions when compiling the patched root QML.
translations={
'Apply':'应用','Autopilot':'AI自动优化','Current settings':'当前设置','Preset':'预设','Autopilot preferences...':'AI自动优化 偏好设置...','Open images...':'打开图像...','Close image':'关闭图像','Close selected images':'关闭所选图像','Close all images':'关闭所有图像','Show in finder':'打开所在位置','Show in explorer':'打开所在位置',
'Confirmation':'确认','Cancel':'取消','Delete':'删除','Cloud rendering':'云端处理','Done':'完成','Autopilot confirmation':'AI自动优化 确认','Continue':'继续','No updates available':'没有可用的更新','Plugin Error':'插件错误','Contact support':'联系支持','Check document':'查看文档','Cleared model cache':'模型缓存已清理','Close':'关闭','Unable to clear model cache':'无法清理模型缓存','License selection':'许可证选择','Got it':'知道了','Save changes':'保存更改','Always do this':'总是这样做',"Don't save":'不保存','Save and exit':'保存并退出','Beta period ended':'测试期已结束','Close Application':'关闭程序','Crash recovery':'崩溃恢复','Start new session':'开始新的会话','Resume':'重启会话','Help':'帮助','View tutorials':'查看教程','Learn about features':'了解功能','Open log folder':'打开日志文件夹','BETA':'测试','Crop unsupported in plugin mode':'插件模式下不支持裁剪','Error downloading installer':'下载安装程序出错','Duplicate filter added':'添加了重复滤镜',
'Unlimited cloud rendering is not available at this moment.':'暂时无法使用无限云端处理。','You can still use your cloud credits to process images in the cloud.':'您仍可以使用云积分在云端处理图像。',
'Are you sure you want to apply Autopilot?':'您确定要应用 AI自动优化 吗？','All enhancements on this photo will be replaced.':'该照片上的所有增强效果将被替换。','Enable Autopilot for all new images?':'为所有新图像启用 AI自动优化？','Autopilot will automatically add enhancements based on an analysis of your image.':'AI自动优化 将根据对您图像的分析自动添加增强功能。','Enable Autopilot for new images':'为新图像启用 AI自动优化',
'You are running the latest version of the software':'您正在运行软件的最新版本','Error running model with plugin workflows':'使用插件工作流运行模型时出错','Please check the support documentation for a potential solution.':'请查阅支持文档以寻找可能的解决方案。','If issue persists, contact Topaz Labs support team.':'如果问题仍然存在，请联系 Topaz Labs 支持团队。','Model cache has successfully been cleared.':'模型缓存已成功清理。','Unable to clear model cache.':'无法清理模型缓存。','Great! Now choose which license you want to use.':'太好了！现在请选择您想要使用的许可证。','Unlimited cloud processing is here!':'无限云端处理功能来了！','Enjoy faster processing speed in the cloud with generative models! You can still use cloud credits inside Topaz Video and with the Video Upscale web tool.':'在云端使用生成模型，享受更快的处理速度！您仍可在 Topaz Video 以及 Video Upscale 网页工具中使用云积分。',
'Are you sure you want to exit? Any unsaved changes will be lost.':'您确定要退出吗？任何未保存的更改都将丢失。','Save settings and open these images next time?':'保存设置，下一次再打开这些图像吗？','Topaz Photo will now remember your settings and load any open images on next launch.':'Topaz Photo 现在将记住您的设置，并在下次启动时自动加载任何已打开的图像。','Please use a released version of Topaz Photo':'请使用正式发布的 Topaz Photo 版本','Open beta session has ended for current version you are using. Please use a released version of the application.':'当前版本的公开测试已结束，请使用正式发布的版本。',
'Do you want to reopen your images and resume your session?':'您想重新打开图像并恢复会话吗？','Looks like Topaz Photo crashed... Resume your session to open any previous images and recover your settings.':'检测到 Topaz Photo 上次异常退出！恢复之前的会话可以重新打开之前的图片并恢复设置。','If you start a new session all previous edits and image processing will be lost.':'如果您开始一个新会话，之前所有的编辑和图像处理将会丢失。','Are you sure you want to apply Autopilot settings to all selected images?':'您确定要将 AI自动优化 设置应用于所有选定的图像吗？','Are you sure you want to apply Autopilot settings to your image?':'您确定要将 AI自动优化 设置应用到您的图像？','This will overwrite existing settings and cannot be undone.':'这将覆盖现有设置，且无法撤销。','Are you sure you want to apply the currently-displayed image settings to all selected images?':'您确定要将当前显示的图像设置应用于所有选定的图像吗？','Are you sure you want to close this image? Any unsaved changes will be lost.':'您确定要关闭此图像吗？所有未保存的更改将丢失。','Are you sure you want to close all selected images?':'您确定要关闭所有选定的图像吗？','Are you sure you want to close all images?':'确定要关闭所有图像吗？','Unsaved changes will be discarded in all selected images. You will not be able to undo this action.':'所有选定的图像中的未保存更改将被丢弃。您将无法撤消此操作。','Unsaved changes will be discarded in all opened images. You will not be able to undo this action.':'所有打开的图像中的未保存更改将被丢弃。您将无法撤消此操作。','Could not open one or more images due to unsupported file types.':'由于不支持的文件类型，无法打开一个或多个图像。','Adjust Lighting and Balance Color enhancements will not save to DNG output correctly. Any RAW files using these enhancements will be saved as TIFF instead.Do you still wish to save?':'光照调整和色彩平衡增强功能无法正确保存为 DNG。使用这些增强功能的 RAW 文件将保存为 TIFF。是否继续保存？','An error occurred when trying to show the file.':'尝试显示文件时发生错误。','Cannot open file: ':'无法打开文件：','Are you sure you want to delete <i>':'您确定要删除 <i>',
'Crop is currently unsupported from plugins that cannot resize the image.':'当前不支持来自无法调整图像尺寸的插件的裁剪操作。','There was an error downloading or verifying the installer.':'下载或验证安装程序时出现错误。','Export finished':'导出完成'
}
# Short captions are changed only in text/title properties, avoiding internal enum or model keys.
for en,zh in translations.items():
 quoted=json.dumps(en,ensure_ascii=False);repl=json.dumps(zh,ensure_ascii=False)
 if len(en)>24 or en.endswith('...'):
  s=s.replace(quoted,repl)
 else:
  s=re.sub(r'((?:text|title)\s*:\s*(?:qsTr\()?)'+re.escape(quoted),lambda m:m.group(1)+repl,s)
s=s.replace('WButton.Size.Compact','WButton.Compact')
s=s.replace('    color: WonderStyle.color.pageBkg','    color: "transparent"',1)
hook='''
        var micaPath=Qt.application.arguments[0].replace(/\\\\/g,"/");
        var micaComponent=Qt.createComponent("file:///"+micaPath.substring(0,micaPath.lastIndexOf("/")+1)+"MicaTheme.qml");
        if(micaComponent.status===Component.Ready) micaComponent.createObject(appWindow,{targetWindow:appWindow,agent:windowAgent,titleItem:titleBar.item});
        else console.warn(micaComponent.errorString());
'''
s=s.replace('        windowAgent.setup(appWindow);','        windowAgent.setup(appWindow);'+hook,1)
s='\n'.join(line for line in s.splitlines() if not line.lstrip().startswith('//'))+'\n'
p=593443304;old=int.from_bytes(b[p-8:p-4],'big');raw=s.encode();packed=len(raw).to_bytes(4,'big')+zlib.compress(raw,9);assert len(packed)<old
b[p-4:p-4+old]=packed+b' '*(old-len(packed));b[p-8:p-4]=len(packed).to_bytes(4,'big')
k='/qt/qml/imageenhance/main.qml'.encode('utf-16le');pos=b.find(k);assert pos>=0 and b.find(k,pos+1)<0;b[pos+len(k)-2:pos+len(k)]=b'x\0'
expected_output="b3cf6ec0a8b0a1ebbf4b2fe8c21030b06428b1218d475e07d209b3d56e694174"
actual=hashlib.sha256(b).hexdigest()
if actual!=expected_output:
    parser.error("Patched output does not match the recorded final SHA-256; no output was written.")
with args.output.open("xb") as output:
    output.write(b)
print("Patched executable:", args.output)
print("SHA-256:", actual)
