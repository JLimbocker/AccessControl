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
