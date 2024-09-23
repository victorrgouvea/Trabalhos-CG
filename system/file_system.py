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
            return

        objects = []
        name = ''
        obj_type = None  # Evitar conflito com palavra reservada 'type'
        color = None
        points = []

        for line in obj_file:
            line = line.strip()  # Remove espaços em branco e quebras de linha
            if len(line) == 0:
                # Se encontrar uma linha vazia, salvar o objeto atual e resetar os valores
                if name or points:
                    objects.append({'name': name, 'type': obj_type, 'points': points, 'color': color})
                name = ''
                obj_type = None
                color = None
                points = []
                continue

            data = line.split()

            if len(data) > 0:
                # Se for um comentário
                if data[0].startswith('#'):
                    comment = line[1:].strip()  # Remove o '#' e qualquer espaço
                    if obj_type is None and comment:  # Captura o tipo do objeto na primeira linha de comentário
                        obj_type = comment
                    elif comment.startswith('(') and comment.endswith(')'):
                        try:
                            color = tuple(map(float, comment.strip('()').split(',')))
                        except ValueError:
                            print(f"Erro ao converter a cor: {comment}")
                            color = None
                    continue  # Ignora comentários

                # Usar `match` para processar tipos de dados como `o`, `v`
                match data[0]:
                    case 'o':
                        name = data[1]
                    case 'v':
                        if len(data) >= 3:
                            points.append((float(data[1]), float(data[2])))

        # Adiciona o último objeto se ele não tiver sido adicionado
        if name or points:
            objects.append({'name': name, 'type': obj_type, 'points': points, 'color': color})

        # Exibe os objetos processados
        for obj in objects:
            print(obj)
            created_object = self.root.display_file.add_object(obj['name'], obj['type'], obj['points'], obj['color'])

            self.root.display_file_interface.add_row(obj['name'], obj['type'], created_object)

            self.root.view_port.force_redraw()

    def save_file(self, path, objects):
        with open(path, 'w', encoding='utf-8') as file:
            for obj in objects:
                file.write(f'# {obj.type}\n')
                file.write(f'# {obj.color}\n')
                file.write(f'o {obj.name}\n')
                for point in obj.coordinates:
                    file.write(f'v {point[0]} {point[1]}\n')
                file.write('\n')
