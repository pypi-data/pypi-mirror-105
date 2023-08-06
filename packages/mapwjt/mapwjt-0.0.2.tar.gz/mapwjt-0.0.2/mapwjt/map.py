class BSTMap:
    class _Node:
        def __init__(self,key=None,value=None):
            self.key=key
            self.value=value
            self.left=None
            self.right=None
        def __str__(self):
            return "key:{},Value:{}".format(str(self.key),str(self.value))
    def __init__(self):
        self._size=0
        self._root=None
    def get_size(self):
        return self._size
    def add(self,key,value):
        self._root=self._add(self._root,key,value)
    def _add(self,node,key,value):
        if not node:
            self._size+=1
            node=self._Node(key,value)
        elif node.key==key:
            node.value=value
        elif node.key>key:
            node.left=self._add(node.left,key,value)
        elif node.key<key:
            node.right=self._add(node.right,key,value)
        return node
    def _get_node(self,node,key):
        if not node:
            return None
        elif node.key==key:
            return node
        elif node.key>key:
            return self._get_node(node.left,key)
        else:
            return self._get_node(node.right,key)
    def exist(self,key):
        return self._get_node(self._root,key) is not None
    def get(self,key):
        node=self._get_node(self._root,key)
        return node.value if node is not None else None
    def set(self,key,value):
        node=self._get_node(self._root,key)
        if not node:
            raise ValueError('key{},doesn\'t exist'.format(str(key)))
        node.value=value
    def remove(self,key):
        node=self._get_node(self._root,key)
        if node != None:
            self._root=self._remove(self._root,key)
            return node.value
        else:
            return None
    def _remove(self,node,key):
        if not node:
            return
        if node.key>key:
            node.left=self._remove(node.left,key)
            return node
        elif node.key<key:
            node.right=self._remove(node.right,key)
            return node
        else:
            if not node.left:
                ret_node=node.right
                node.right=None
                self._size-=1
                return ret_node
            elif not node.right:
                ret_node=node.left
                node.left=None
                self._size-=1        
                return ret_node
            else:
                ret_node=self._minimum(node.right)
                ret_node.right=self._remove_min(node.right)
                ret_node.left=node.left
                node.left=node.right=None
                return ret_node
    def _minimum(self,node):
        if not node.left:
            return node
        
        return self._minimum(node.left)
    def _remove_min(self,node):
        if not node.left:
            ret_node=node.right
            node.right=None
            self._size-=1
            return ret_node
        node.left=self._remove_min(node.left)
        return node

