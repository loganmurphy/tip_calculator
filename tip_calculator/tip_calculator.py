import tornado.ioloop
import tornado.web

class MainHandler(tornado.web.RequestHandler):
  def get(self):
    self.set_header("Content-Type", 'html')


class TipCalculator(tornado.web.RequestHandler):
  def post(self):
      bill = self.get_body_argument('bill')
      service = self.get_body_argument('service')
      if bill[0] == '$':
         tip = int(bill[1:]) * float(service)
         self.write("Your tip should be ${}".format(tip))
      elif bill[0]  in ('1234567890'):
          tip = int(bill) * float(service)
          self.write("Your tip should be ${}".format(tip))
          tip2 = tip
      else:
          self.write("Invalid input")

  def get(self):
    self.set_header(
      'Cache-Control',
      'no-store, no-cache, must-revalidate, max-age=0')
    self.render('tip_calculator.html')

def make_app():
  return tornado.web.Application([
    (r"/", TipCalculator),
    (r"/static/(.*)", tornado.web.StaticFileHandler, {'path': 'static'})
  ], autoreload=True)


if __name__ == "__main__":
  tornado.log.enable_pretty_logging()
  app = make_app()
  app.listen(8888)
  tornado.ioloop.IOLoop.current().start()
