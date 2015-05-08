#Notes
General notes and code snippets that I find helpful or necessary.

##Pronterface Code of Interest

###Print Status Methods
These little snippets are probably where I would pass off status of a print
so we can log that on the database.

####File: pronterface.py - printrun
####Line: 1421

```python
def output_gcode_stats(self):
  gcode = self.fgcode
  self.log(_("%.2fmm of filament used in this print") % gcode.filament_length)
  self.log(_("The print goes:"))
  self.log(_("- from %.2f mm to %.2f mm in X and is %.2f mm wide") %
    (gcode.xmin, gcode.xmax, gcode.width))
  self.log(_("- from %.2f mm to %.2f mm in Y and is %.2f mm deep") %
    (gcode.ymin, gcode.ymax, gcode.depth))
  self.log(_("- from %.2f mm to %.2f mm in Z and is %.2f mm high") %
    (gcode.zmin, gcode.zmax, gcode.height))
  self.log(_("Estimated duration: %d layers, %s") %
    gcode.estimate_duration())
```
####File: pronterface.py - printrun
####Line: 883

```python
def update_recent_files(self, param, value):
    if self.filehistory is None:
        return
    recent_files = []
    try:
        recent_files = json.loads(value)
    except:
        self.logError(_("Failed to load recent files list:") +
                      "\n" + traceback.format_exc())
    # Clear history
    while self.filehistory.GetCount():
        self.filehistory.RemoveFileFromHistory(0)
    recent_files.reverse()
    for f in recent_files:
        self.filehistory.AddFileToHistory(f)
```
####File: pronterface.py - printrun
####Line: 1302

```python
def load_recent_file(self, event):
    fileid = event.GetId() - wx.ID_FILE1
    path = self.filehistory.GetHistoryFile(fileid)
    self.loadfile(None, filename = path)

def loadfile(self, event, filename = None):
    if self.slicing and self.slicep is not None:
        self.slicep.terminate()
        return
    basedir = self.settings.last_file_path
    if not os.path.exists(basedir):
        basedir = "."
        try:
            basedir = os.path.split(self.filename)[0]
        except:
            pass
    dlg = None
    if filename is None:
        dlg = wx.FileDialog(self, _("Open file to print"), basedir, style = wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        dlg.SetWildcard(_("OBJ, STL, and GCODE files (*.gcode;*.gco;*.g;*.stl;*.STL;*.obj;*.OBJ)|*.gcode;*.gco;*.g;*.stl;*.STL;*.obj;*.OBJ|All Files (*.*)|*.*"))
    if filename or dlg.ShowModal() == wx.ID_OK:
        if filename:
            name = filename
        else:
            name = dlg.GetPath()
            dlg.Destroy()
        if not os.path.exists(name):
            self.statusbar.SetStatusText(_("File not found!"))
            return
        path = os.path.split(name)[0]
        if path != self.settings.last_file_path:
            self.set("last_file_path", path)
        try:
            abspath = os.path.abspath(name)
            recent_files = []
            try:
                recent_files = json.loads(self.settings.recentfiles)
            except:
                self.logError(_("Failed to load recent files list:") +
                              "\n" + traceback.format_exc())
            if abspath in recent_files:
                recent_files.remove(abspath)
            recent_files.insert(0, abspath)
            if len(recent_files) > 5:
                recent_files = recent_files[:5]
            self.set("recentfiles", json.dumps(recent_files))
        except:
            self.logError(_("Could not update recent files list:") +
                          "\n" + traceback.format_exc())
        if name.lower().endswith(".stl") or name.lower().endswith(".obj"):
            self.slice(name)
        else:
            self.load_gcode_async(name)
    else:
        dlg.Destroy()
```
