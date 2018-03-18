import platform

if platform.system() == 'Darwin':
    from .settingsStore.dev import *
elif platform.system() == 'Linux':
    from .settingsStore.prod import *
else:
    from .settingsStore.dev import *
