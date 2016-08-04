from pylons import url
import simplejson as json

class MenuReader:
    def __init__(self):
        self._menu = []
        self.read_data('menu_data.json')

    def read_data(self,file):
        try:
           self._menu = json.load(open(file,'r'))
        except Exception, e:
           pass

    def get_jsonmenu(self):
	return self._menu

    def get_menu(self,menu_item=None):
        menu_item = menu_item or []
        menu = self._menu
        menu_item = [menu_item] if type(menu_item).__name__ == 'str' else menu_item
        for item in menu_item:
            for i in menu:
                if item == i['title']:
                    menu = i.get('submenu',[])
                    break
        return [ (i['title'],url(controller=i['controller'],action=i['action']),i.get('auth',False)) for i in menu ]

    def find_menu(self,controller,action,layer=None):
        a = self._traverse(controller,action)
        return self.get_menu(a[:layer]) if a else []
        
    def find_title(self,controller,action,layer=None):
        a = self._traverse(controller,action) or []
        return a[layer-1] if layer < len(a) else ''
        
    def _traverse(self,controller,action='index',start=None):
        start = self._menu if not start else start.get('submenu', [])
        for i in start:
            if controller == i.get('controller') and action == i.get('action'):
                return [i.get('title')]
            path = self._traverse(controller,action,i)
            if path:
                return [i.get('title')] + path
            
            
