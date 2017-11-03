import os
import boto3


import tornado.ioloop
import tornado.web
import tornado.log

from jinja2 import \
  Environment, PackageLoader, select_autoescape

# This allows jinja to find my templates;
ENV = Environment(
  loader=PackageLoader('app', 'templates'),
  autoescape=select_autoescape(['html', 'xml'])
)

# This class allows for rendering templates
class TemplateHandler(tornado.web.RequestHandler):
  def render_template (self, tpl, context):
    template = ENV.get_template(tpl)
    self.write(template.render(**context))

class TipCalculator(TemplateHandler):
  def get(self):
    self.set_header(
      'Cache-Control',
      'no-store, no-cache, must-revalidate, max-age=0')
    self.render_template('tip_calculator.html', {})
    # I did the logic here initially, then I added in JQuery on the front end so I switched it out.
  # def post(self):
  #     bill = self.get_body_argument('bill')
  #     service = self.get_body_argument('service')
  #     if bill[0] == '$':
  #        tip = int(bill[1:]) * float(service)
  #        self.write("Your tip should be ${}".format(tip))
  #     elif bill[0]  in ('1234567890'):
  #         tip = int(bill) * float(service)
  #         self.write("Your tip should be ${}".format(tip))
  #       #   tip2 = tip
  #     else:
  #         self.write("Invalid input")


# This runs the app and assigns page handlers
def make_app():
  return tornado.web.Application([
    (r"/", TipCalculator),
    (r"/static/(.*)", tornado.web.StaticFileHandler, {'path': 'static'})
  ], autoreload=True)


# This stuff won't be run if someone imports my module
if __name__ == "__main__":
  tornado.log.enable_pretty_logging()
  app = make_app()
  app.listen(int(os.environ.get('PORT', '8888')))
  print("All systems are go! App now up and running on PORT 8888!")
  tornado.ioloop.IOLoop.current().start()
