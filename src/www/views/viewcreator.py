
class ViewCreator(object):
    
    @classmethod
    def create_view(cls, controller):
        controller.before_create_view()
        view = controller.create_view()
        controller.after_create_view()
        
        view.set_headers()
        
        view.before_build_output()
        view.build_output()
        view.after_build_output()
        
        return view.output

