def get_path(dirlist: list) -> str:
    if len(dirlist) == 0: return ''
    return '/'.join(dirlist) + '/'

class Directory:
    def __init__(self, path, shortname) -> None:
        self.subdirs = set([])
        self.files = set([])
        if shortname == '': self.name = '/' 
        else: self.name = '/' + path + shortname + '/'
        self.shortname = shortname

class File:
    def __init__(self, path: list, name: str, size:int) -> None:
        self.path = path
        self.name = name
        self.size = size

class Fs_inst:
    def cd(self, parent, dir):
        if dir == '..':
            parent.workingdir.pop()
        elif dir == '/':
            parent.workingdir = []
        else:
            path = get_path(parent.workingdir)
            parent.dirs.setdefault('/' + path+dir+'/',Directory(path, dir))
            parent.workingdir.append(dir)

    def ls():
        pass

    def __init__(self) -> None:
        pass

class Dos:
    def init_command(self) -> dict:
        run_command = {}

        
        run_command['cd'] = self.fs_inst.cd
        run_command['ls'] = self.fs_inst.ls

        return run_command

    def __init__(self) -> None:
        self.workingdir = ['']

        self.fs_inst = Fs_inst()
        self.run_command = self.init_command()
        self.dirs = {'/': Directory('','')}
        
    def read_batch(self, file):
        with open(file, 'r') as f:
            for line in f:
                command = line.strip().split(' ')
                if command[0] == '$':
                    #self.run_command[command[1]]
                    if command[1] == 'cd': self.fs_inst.cd(self, command[2])
                if command[0] == 'dir': #oletetaan, että näitä voi tulla vain ls:n perässä
                    newdir = self.workingdir.copy()
                    newdir.append(command[1])
                    self.dirs.setdefault('/' + get_path(newdir),Directory(get_path(self.workingdir),command[1]))
                    self.dirs['/' + get_path(self.workingdir)].subdirs.add(command[1]+'/')
                if command[0].isnumeric():
                    newfile = File(self.workingdir,command[1],int(command[0]))
                    self.dirs['/'+get_path(self.workingdir)].files.add(newfile)

    def get_size(self, directory):
        totsize = 0
        for file in self.dirs[directory].files:
            totsize += file.size
        for dir in self.dirs[directory].subdirs:
            totsize += self.get_size(directory + dir)
        return totsize

    def get_all_size(self) -> dict:
        sizes = {}
        for dir in self.dirs:
            sizes[self.dirs[dir].name] = self.get_size(self.dirs[dir].name)
        return sizes