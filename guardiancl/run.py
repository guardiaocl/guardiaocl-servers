import sys
import os
import json
import logging.config

import configparser2

import console
import guardianService


class GuardianCl(object):
    def __init__(self, args):
        self.app = self._create_app(args)
        self._setup_logging()
        self._setup_system()

    def _create_app(self, args):
        app = {'args': args}
        return app

    def _setup_system(self):
        config_path = os.path.abspath("system.ini")
        if not os.path.exists(config_path):
            config = configparser2.ConfigParser()
            config.add_section('ROUTES')
            config.set('ROUTES', 'auth', 'http://localhost:3000/service/v1/authenticate')
            config.set('ROUTES', 'devices', 'http://localhost:3000/service/v1/devices')
            config.set('ROUTES', 'collect', 'http://localhost:3000/collect')

            with open(config_path, 'w') as configfile:
                config.write(configfile)

    def _setup_logging(self):
        config_path = os.path.abspath("logging.json")
        if os.path.exists(config_path):
            with open(config_path) as f:
                config = json.load(f)
            logging.config.dictConfig(config)

    def _run_option(self):
        console.clear()
        args = self.app['args']
        if len(args[0:1]) >= 1:
            for opt in args[0:1]:
                if opt in ['-h','help']:
                    self._usage()
                    sys.exit(2)
                elif opt == "configure":
                    sub_opt = args[1:]
                    if not os.path.exists('config.cfg'):
                        guardianService.create_config_file()
                    elif not sub_opt:
                        guardianService.update_config_file()
                    elif len(sub_opt) == 1:
                        if sub_opt[0] == 'disk':
                            guardianService.update_config_file("DISK")
                        elif sub_opt[0] == 'inet':
                            guardianService.update_config_file("NET_INTERFACE")
                        else:
                            self._usage()
                    else:
                        self._usage()
                elif opt == "list":
                    sub_opt = args[1:]
                    if sub_opt:
                        if sub_opt[0] == "disk" or sub_opt[0] == "inet":
                            guardianService.list_configs(sub_opt[0])
                    else:
                        self._usage()
                elif opt == "monitor":
                    guardianService.start_monitor()
                else:
                    self._usage()
        elif len(args) < 1:
            self._usage()

    def _usage(self):
        print('  Usage: python run.py [command]'
              '\n\n  Commands:'
              '\n\n    configure [ disk | inet ]         |  config client'
              '\n    monitor                           |  start monitoring'
              '\n    list [ disk | inet ]              |  list disk or inet config'
              '\n    help                              |  show usage\n')

    def run(self):
        self._run_option()

def main():
    start = GuardianCl(sys.argv[1:])
    start.run()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
