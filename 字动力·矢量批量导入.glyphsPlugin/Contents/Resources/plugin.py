import sys
from pathlib import Path
import objc
from GlyphsApp import Glyphs,EDIT_MENU
from GlyphsApp.plugins import GeneralPlugin
from AppKit import NSMenuItem

class SVGBatchImportPlugin(GeneralPlugin):
    @objc.python_method
    def settings(self): self.name='字动力 · 矢量批量导入'
    @objc.python_method
    def start(self):
        if getattr(self,'_svg_menu_item',None) is not None:return
        item=NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(self.name,self.showWindow_,'')
        item.setTarget_(self);Glyphs.menu[EDIT_MENU].append(item);self._svg_menu_item=item
    def showWindow_(self,sender):
        resources=Path(__file__).resolve().parent
        import platform
        if sys.implementation.cache_tag!='cpython-311' or platform.machine()!='arm64':
            from GlyphsApp import Message
            Message('此内测包需要CPython 3.11和Apple Silicon；请使用已验证环境助手。不会改动工程或字体。','运行环境不匹配')
            return
        # Host Python/PyObjC are prerequisites. Use existing Vanilla if present,
        # otherwise load the bundled MIT copy; never register a second copy.
        runtime=str(resources/'runtime.zip')
        if runtime not in sys.path:sys.path.insert(0,runtime)
        try:
            from svg_batch._write_gate import check_installation
            check_installation()
        except Exception as exc:
            from GlyphsApp import Message
            Message(str(exc),'插件完整性检查失败')
            return
        import vanilla
        from svg_batch.storage import prepare
        prepare()
        from svg_batch.runtime_compat import check_launch
        if not check_launch():return
        from svg_batch.panel import show_panel
        self.panel=show_panel(getattr(self,'panel',None))
    @objc.python_method
    def __file__(self):return __file__
