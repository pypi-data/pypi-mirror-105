def get(filename):
    if not filename.__contains__(".py"):
        filename += ".py"

    with open(filename, "w") as f:
        with open("PygameTemplates/basic.py", "r") as b:
            f.writelines(b.readlines())
