from ipytree import Tree, Node
import ipywidgets as widgets
from ipywidgets import interactive
import os

def file_tree():
    # create widgets as a simple file browser
    full_widget = widgets.HBox()
    left_widget = widgets.VBox()
    right_widget = widgets.VBox()

    path_widget = widgets.Text()
    path_widget.layout.min_width = '300px'
    select_widget = widgets.Button(
      description='Select', button_style='primary', tooltip='Select current media file.'
      )
    drive_url = widgets.Output()

    right_widget.children = [select_widget]
    full_widget.children = [left_widget]

    tree_widget = widgets.Output()
    tree_widget.layout.max_width = '300px'
    tree_widget.overflow = 'auto'

    left_widget.children = [path_widget,tree_widget]

    # init file tree
    my_tree = Tree(multiple_selection=False)
    my_tree_dict = {}
    media_names = []

    def select_file(b):
        global drive_dir 
        drive_dir = path_widget.value
        # full_widget.disabled = True
        clear_output()
        print('File selected，please execute next cell')
        print('已选择文件，请执行下个单元格')
    #     if (out_file not in my_tree_dict.keys()) and (out_dir in my_tree_dict.keys()):
    #         node = Node(os.path.basename(out_file))
    #         my_tree_dict[out_file] = node
    #         parent_node = my_tree_dict[out_dir]
    #         parent_node.add_node(node)

    select_widget.on_click(select_file)

    def handle_file_click(event):
        if event['new']:
            cur_node = event['owner']
            for key in my_tree_dict.keys():
                if (cur_node is my_tree_dict[key]) and (os.path.isfile(key)):
                    try:
                        with open(key) as f:
                            path_widget.value = key
                            path_widget.disabled = False
                            select_widget.disabled = False
                            full_widget.children = [left_widget, right_widget]
                    except Exception as e:
                        path_widget.value = key
                        path_widget.disabled = True
                        select_widget.disabled = True

                        return

    def handle_folder_click(event):
        if event['new']:
            full_widget.children = [left_widget]

    # redirect cwd to default drive root path and add nodes
    my_dir = '/drive/MyDrive'
    my_root_name = my_dir.split('/')[-1]
    my_root_node = Node(my_root_name)
    my_tree_dict[my_dir] = my_root_node
    my_tree.add_node(my_root_node)
    my_root_node.observe(handle_folder_click, 'selected')

    for root, d_names, f_names in os.walk(my_dir):
        folders = root.split('/')
        for folder in folders:
            if folder.startswith('.'):
                continue
        for d_name in d_names:
            if d_name.startswith('.'):
                d_names.remove(d_name)
        for f_name in f_names:
            if f_name.lower().endswith(('mp3','m4a','flac','aac','wav','mp4','mkv','ts','flv')):
                media_names.append(f_name)

        d_names.sort()
        f_names.sort()
        media_names.sort()
        keys = my_tree_dict.keys()

        if root not in my_tree_dict.keys():
          # print(f'root name is {root}') # folder path
          name = root.split('/')[-1] # folder name
          # print(f'folder name is {name}')
          dir_name = os.path.dirname(root) # parent path of folder
          # print(f'dir name is {dir_name}')
          parent_node = my_tree_dict[dir_name]
          node = Node(name)
          my_tree_dict[root] = node
          parent_node.add_node(node)
          node.observe(handle_folder_click, 'selected')

        if len(media_names) > 0:
              parent_node = my_tree_dict[root] # parent folders
              # print(parent_node)
              parent_node.opened = False
              for f_name in media_names:
                  node = Node(f_name)
                  node.icon = 'file' 
                  full_path = os.path.join(root, f_name)
                  # print(full_path)
                  my_tree_dict[full_path] = node
                  parent_node.add_node(node)
                  node.observe(handle_file_click, 'selected')
        media_names.clear()

    with tree_widget:
      tree_widget.clear_output()
      display(my_tree)

    return full_widget