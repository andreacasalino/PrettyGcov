from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
from urllib.parse import urlparse
from urllib.parse import parse_qs

from PrettyGcov.CoverageMap import CoverageMap
from PrettyGcov.CoverageTree import makeCoverageTree
from PrettyGcov.WebServer.PageFactory import PageFactory

class ReportHandler(BaseHTTPRequestHandler):
    def sendResponse_(self, response_content: str, kind=None):
        if kind == None:
            kind = 'text/html'
        self.send_response(200)
        self.send_header('Content-type', kind)
        self.end_headers()
        self.wfile.write(response_content.encode("utf-8"))

    def servePage_(self, path: list[str]):
        logging.info('SERVE element with path {}'.format(path))
        page = self.server.pageFactory.makePage(path)
        self.sendResponse_(page)

    def do_GET(self):
        logging.info('GET {}'.format(self.path))

        if self.path == '/':
            rootPath = self.server.pageFactory.coverageTree_.path_
            self.servePage_(rootPath)

        elif self.path == '/favicon.ico':
            self.sendResponse_('', kind='text')

        elif self.path.find('/element') == 0:
            def getParameters(path):
                parse_result = urlparse(path)
                parameters = parse_qs(parse_result.query)
                return parameters

            parameters = getParameters(self.path)
            path = parameters['slice']
            self.servePage_(path)

        else:
            self.send_response(404)

class ReportServer(HTTPServer):
    def __init__(self, *args, **kw):
        self.pageFactory = None
        HTTPServer.__init__(self, *args, **kw)

from optparse import OptionParser

def runServer(port: int, verbose: bool, gcovFileFolder: str, srcFolders: list[str]):
    logging.basicConfig(level=logging.INFO)

    logging.info('Reading gcov files from {}'.format(gcovFileFolder))
    for srcFolder in srcFolders:
        logging.info('Accepting source files from {}'.format(srcFolder))

    coverage_map = CoverageMap(gcovFileFolder)
    if verbose:
        coverage_map.verbosity()
    for srcFolder in srcFolders:
        coverage_map.addSourceDirectory(srcFolder)
    coverage_map.generate()

    coverage_tree = makeCoverageTree(coverage_map)

    server_address = ('', port)
    server = ReportServer(server_address, ReportHandler)
    server.pageFactory = PageFactory(port, coverage_tree)

    logging.info('Starting report server on port {} ...'.format(port))
    logging.info('Copy paste to your browser the following address: http://localhost:{}/'.format(port))
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    server.server_close()
    logging.info('Stopping report server...')

def main():
    parser = OptionParser()
    parser.add_option("-p", "--port", default=8080)
    parser.add_option("-v", "--verbosity", default=False)
    parser.add_option("-g", "--gcov_root", help="folder storing the gcda files")
    parser.add_option("-s", "--src_root", help="folder storing the source files")
    options, args = parser.parse_args()

    runServer(int(options.port), options.verbosity, options.gcov_root, [options.src_root])

if __name__ == "__main__":
    main()
