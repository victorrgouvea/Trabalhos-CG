from pathlib import Path

class FileSystem():

    def __init__(self, root):
        self.root = root

    def load_mtl_file(self, mtl_path):
        materials = {}
        current_material = None

        try:
            with open(mtl_path, 'r', encoding='utf-8') as file:
                for line in file:
                    line = line.strip()
                    if line.startswith('newmtl'):
                        current_material = line.split()[1]  # Nome do material
                        materials[current_material] = None  # Inicializa com cor None
                    elif line.startswith('Kd') and current_material:
                        # Converte os valores de cor para float e cria uma tupla
                        materials[current_material] = tuple(map(float, line.split()[1:]))
        except FileNotFoundError:
            print(f'Material file {mtl_path} not found')
    
        return materials

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
        obj_type = None
        color = None
        points = []
        materials = {}  # Dicionário para armazenar materiais
        current_material = None  # Material atualmente em uso

        for line in obj_file:
            line = line.strip()

            if len(line) == 0:  # Se encontrar uma linha vazia, finalize o objeto anterior
                if len(points) == 1:
                    obj_type = 'point'
                elif len(points) == 2:
                    obj_type = 'line'
                else:
                    obj_type = 'wireframe'

                if name or points:
                    print(name, obj_type, points, color)
                    objects.append({'name': name, 'type': obj_type, 'points': points, 'color': color})
                name = ''
                points = []
                continue

            data = line.split()

            if len(data) > 0:
                match data[0]:
                    case 'mtllib':
                        path_obj = Path(path)
                        mtl_path = data[1]
                        materials = self.load_mtl_file(path_obj.parent / mtl_path)
                    case 'usemtl':
                        current_material = data[1]
                        color = materials.get(current_material, None)
                        if color is None:
                            color = (0, 0, 0)
                    case 'o':
                        name = data[1]
                    case 'v':
                        if len(data) >= 3:
                            points.append((float(data[1]), float(data[2]), float(data[3])))

        # Adiciona o último objeto se ele não tiver sido adicionado
        if name or points:
            objects.append({'name': name, 'type': obj_type, 'points': points, 'color': color})

        # Exibe os objetos processados
        for obj in objects:
            print(obj)
            created_object = self.root.display_file.add_object(obj['name'], obj['type'], obj['points'], obj['color'])
            self.root.display_file_interface.add_row(obj['name'], obj['type'], created_object)
            self.root.drawing_area.force_redraw()

    def save_file(self, path, objects):
        materials = {}
    
        with open(path, 'w', encoding='utf-8') as file:
            mtl_path = path.replace('.obj', '.mtl')
            file.write(f'mtllib {mtl_path.split("/")[-1]}\n')

            for obj in objects:
                file.write(f'o {obj.name}\n')
                file.write(f'usemtl {obj.name}\n')
                for point in obj.coordinates:
                    file.write(f'v {point[0]} {point[1]} {point[2]}\n')
                file.write('\n')
                
                materials[obj.name] = obj.color
        
        self.save_mtl_file(mtl_path, materials)

    def save_mtl_file(self, path, materials):
        with open(path, 'w', encoding='utf-8') as file:
            for material, color in materials.items():
                file.write(f'newmtl {material}\n')
                file.write(f'Kd {color[0]} {color[1]} {color[2]}\n')
                file.write('\n')
