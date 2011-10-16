import time
import re

from logster_helper import MetricObject, LogsterParser
from logster_helper import LogsterParsingException

class ApacheErrorLogster(LogsterParser):

    def __init__(self, option_string=None):

        self.stats = {'php_fatal':        0,
                     'php_warning':       0,
                     'php_parse':         0,
                     'file_not_exists':   0,
                     'seg_fault':         0,
                     'mod_mime_magic':    0,

                     'invalid_method_in_request':    0,
                     'invalid_uri_in_request':       0,
                     'http_1_1_without_hostname':    0,
                     'error_reading_headers':        0,
                     'forbidden_by_options':         0}

        regex = '.*('
        regex+= '(?P<php_fatal>PHP Fatal error)|'
        regex+= '(?P<php_warning>PHP Warning)|'
        regex+= '(?P<php_parse>PHP Parse error)|'
        regex+= '(?P<file_not_exists>File does not exist)|'
        regex+= '(?P<seg_fault>signal Segmentation fault)|'
        regex+= '(?P<mod_mime_magic>mod_mime_magic)|'
        regex+= '(?P<invalid_method_in_request>Invalid method in request)|'
        regex+= '(?P<invalid_uri_in_request>Invalid URI in request)|'
#        regex+= '(?P<http_1_1_without_hostname>HTTP/1.1 request without hostname)|'
        regex+= '(?P<forbidden_by_options>forbidden by Options directive)|'
        regex+= '(?P<error_reading_headers>request failed: error reading the headers)'
        regex+= ').*'

        self.reg = re.compile(regex)


    def parse_line(self, line):

        try:
            regMatch = self.reg.match(line)

            if regMatch:
                linebits = regMatch.groupdict()

                if (linebits['php_fatal']):
                    self.stats['php_fatal'] += 1
                if (linebits['php_warning']):
                    self.stats['php_warning'] += 1
                if (linebits['php_parse']):
                    self.stats['php_parse'] += 1
                if (linebits['file_not_exists']):
                    self.stats['file_not_exists'] += 1

                if (linebits['seg_fault']):
                    self.stats['seg_fault'] += 1
                if (linebits['mod_mime_magic']):
                    self.stats['mod_mime_magic'] += 1

                if (linebits['invalid_method_in_request']):
                    self.stats['invalid_method_in_request'] += 1
                if (linebits['invalid_uri_in_request']):
                    self.stats['invalid_uri_in_request'] += 1
                if (linebits['http_1_1_without_hostname']):
                    self.stats['http_1_1_without_hostname'] += 1
                if (linebits['error_reading_headers']):
                    self.stats['error_reading_headers'] += 1
                if (linebits['forbidden_by_options']):
                    self.stats['forbidden_by_options'] += 1
        except Exception, e:
            raise LogsterParsingException, "regmatch or contents failed with '%s'" % e


    def get_state(self, duration):
        # Return a list of metrics objects
        return [
            MetricObject("php_fatal", (self.stats['php_fatal']), "PHP Errors"),
            MetricObject("php_warning", (self.stats['php_warning']), "PHP Warning"),
            MetricObject("php_parse", (self.stats['php_parse']), "PHP Parse error"),
            MetricObject("file_not_exists", (self.stats['file_not_exists']), "File does not exist"),

            MetricObject("seg_fault", (self.stats['seg_fault']), "Signal segmentation fault"),
            MetricObject("mod_mime_magic", (self.stats['mod_mime_magic']), "mod_mime_magic"),

            MetricObject("invalid_method_in_request", (self.stats['invalid_method_in_request']), "Invalid method in request"),
            MetricObject("invalid_uri_in_request", (self.stats['invalid_uri_in_request']), "Invalid URI in request"),
            MetricObject("http_1_1_without_hostname", (self.stats['http_1_1_without_hostname']), "client sent HTTP/1.1 request without hostname"),
            MetricObject("error_reading_headers", (self.stats['error_reading_headers']), "Directory index forbidden by Options directive"),
            MetricObject("forbidden_by_options", (self.stats['forbidden_by_options']), "Request failed: error reading the headers"),
        ]
