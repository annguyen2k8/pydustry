import zipfile

from pydustry import classpath

with zipfile.ZipFile(classpath) as jar:
    for member in jar.infolist():
        if member.filename.startswith("sprites/"):
            jar.extract(member, "./assets")