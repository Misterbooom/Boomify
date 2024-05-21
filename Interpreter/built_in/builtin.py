import importlib
import os
blocked = ["base_function",'builtin']
module_names = [
    name.replace(".py", "").replace(".py", "")
    for name in os.listdir("Interpreter/built_in")
    if name.endswith(".py") and name.replace(".py", "") not in blocked
]

built_in = []

for module_name in module_names:
    try:
        module = importlib.import_module(f"built_in.{module_name}")

        cls = getattr(module, module_name.capitalize())

        built_in.append(cls)
    except (ImportError, AttributeError) as e:
        print(f"Error importing module '{module_name}': {e}")
