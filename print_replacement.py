import bpy

___print = print
def print(str, clear=False, log_name='_LOG_', log_format="[LOG] {0}\n"):
    if log_name not in bpy.data.texts:
        bpy.data.texts.new(log_name)
    log_target = bpy.data.texts[log_name]
    if clear:
        log_target.clear()
    out = log_format.format(str)
    log_target.write(out)
    ___print(out)

print("Logging Active", clear=True, log_format="=== {0} ===\n")

print(15)
