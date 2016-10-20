from {{appname}}.handlers.base import BaseHandler
from {{appname}}.models.{{handler_name}} import {{handler_model_class_name}}
from {{appname}}.config import application
from {{appname}}.server import app

@app.add_rest_routes("{{handler_name}}")
class {{handler_name}}Handler(BaseHandler):

    # 
    # every pow handler automatically gets these RESTful routes
    #
    # 1  GET    /{{handler_name}}        #=> index
    # 2  GET    /{{handler_name}}/1      #=> show
    # 3  GET    /{{handler_name}}/new    #=> new
    # 4  GET    /{{handler_name}}/1/edit #=> edit 
    # 5  GET    /{{handler_name}}/page/1 #=> page
    # 6  GET    /{{handler_name}}/search #=> search
    # 7  PUT    /{{handler_name}}/1      #=> update
    # 8  POST   /{{handler_name}}        #=> create
    # 9  DELETE /{{handler_name}}/1      #=> destroy

    def show(self, id=None):
        m={{handler_model_class_name}}()
        res=m.find_one({{handler_model_class_name}}.id==id)
        self.success(message="{{handler_model_class_name}} show", data=res.json_dump())

    def index(self):
        m={{handler_model_class_name}}()
        res = m.find_all(as_json=True)
        self.success(message="{{handler_model_class_name}}, index", data=res)         
    
    def page(self, page=0):
        m={{handler_model_class_name}}()
        page_size=application["page_size"]
        res = m.find_all(as_json=True, 
            limit=(page*page_size)+page_size,
            offset=page*page_size
            )
        self.success(message="{{handler_model_class_name}} page: #" +str(page), data=res )  

    @tornado.web.authenticated
    def edit(self, id=None):
        self.success(message="{{handler_model_class_name}}, edit id: " + str(id))

    @tornado.web.authenticated
    def new(self):
        self.success("{{handler_model_class_name}}, new")

    @tornado.web.authenticated
    def create(self):
        self.success(message="{{handler_model_class_name}}, create")

    @tornado.web.authenticated
    def update(self, id=None):
        self.success("{{handler_model_class_name}}, update id: " + str(id))

    @tornado.web.authenticated
    def destroy(self, id=None):
        self.success("{{handler_model_class_name}}, destroy id: " + str(id))
