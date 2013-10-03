import bottle
import pkg_resources

bottle.TEMPLATE_PATH.insert(0,pkg_resources.resource_filename('HackSpark.SimpleDomotics', 'views/'))
app = bottle.default_app()
