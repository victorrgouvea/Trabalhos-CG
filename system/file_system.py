class FileSystem():

    def __init__(self, root):
        self.root = root

    def load_file(self, path):
      obj_file = ''
      try:
          with open(path, 'r', encoding='utf-8') as file:
              obj_file = file.readlines()
      except FileNotFoundError:
          print('File not found')

      objects = []
      name = ''
      points = []
      for line in obj_file:

        data = line.split()

        if len(data) > 0:

            if data[0].startswith('#'):
                continue

            match data[0]:
              case 'o':
                if len(points) > 0:
                    objects.append({'name': name, 'points': points})
                    points = []
                name = data[1]

              case 'v':
                points.append((float(data[1]), float(data[2])))

      if (len(points) > 0) and (name == ''):
          objects.append({'name': '', 'points': points})

      for x in objects:
          print(x)

    def save_file(self, path, objects):
        with open(path, 'w', encoding='utf-8') as file:
            for obj in objects:
                file.write(f'o {obj["name"]}\n')
                for point in obj['points']:
                    file.write(f'v {point[0]} {point[1]}\n')
                file.write('\n')
