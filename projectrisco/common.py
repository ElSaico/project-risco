from tornado.options import parse_config_file, define, options

define("debug", type=bool, default=True)
define("port", type=int, default=8888)
define("cookie")
define("database_name", default="risco")
define("database_uri", default="mongodb://localhost/risco")
define("database_name_test", default="risco-test")
define("database_uri_test", default="mongodb://localhost/risco-test")
parse_config_file("server.conf")
