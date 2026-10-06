import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time
import unittest
from unittest.mock import patch

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'scripts/access_probe.py'
spec = importlib.util.spec_from_file_location('access_probe', SCRIPT)
probe = importlib.util.module_from_spec(spec)
spec.loader.exec_module(probe)

class ProbeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory(prefix='aaa-probe-tests-')
        fake = Path(cls.temp.name) / 'curl'
        fake.write_text('#!' + sys.executable + '\n' + '''import os, pathlib, sys, time
assert sys.argv[1] == '--disable'
assert not any(x in sys.argv for x in ['--cookie', '--cookie-jar', '--header', '--location', '--retry', '--user'])
scenario = os.environ['AAA_PROBE_TEST_SCENARIO']
response_path = pathlib.Path(sys.argv[sys.argv.index('--output')+1])
pathlib.Path(os.environ['AAA_PROBE_TEST_PATH_LOG']).write_text(str(response_path))
if scenario == 'hang':
    response_path.write_bytes(b'%PDF-partial')
    time.sleep(30)
    sys.exit(0)
status, mime, body, code = {
    'html': ('200','text/html',b'<html><title>Unique source</title></html>',0),
    'pdf': ('200','application/pdf',b'%PDF-1.4 test fixture',0),
    'forbidden': ('403','text/html',b'<h1>Forbidden</h1>',0),
    'challenge': ('200','text/html',b'<title>Just a moment...</title>',0),
    'false_pdf': ('200','application/pdf',b'<html>Error document</html>',0),
    'redirect': ('302','text/html',b'',0),
    'oversize': ('200','application/pdf',b'%PDF-',63),
    'oversize_exit_zero': ('200','application/pdf',b'%PDF-'+b'x'*4096,0),
    'curl_timeout': ('200','application/pdf',b'%PDF-partial',28),
    'error': ('500','text/html',b'<title>Server error</title>',0),
}[scenario]
response_path.write_bytes(body)
print(status+'\\n'+mime, end='')
sys.exit(code)
''')
        fake.chmod(0o700)
        cls.path_log = Path(cls.temp.name) / 'response_path.txt'
        cls.env = {**os.environ, 'PATH': str(Path(cls.temp.name)) + os.pathsep + os.environ.get('PATH', ''),
                   'AAA_PROBE_TEST_PATH_LOG': str(cls.path_log)}

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def run_cli(self, scenario, *args):
        run = subprocess.run([sys.executable, str(SCRIPT), 'https://aaa.org.hk/en/collections/search', *args],
            capture_output=True, text=True, env={**self.env, 'AAA_PROBE_TEST_SCENARIO': scenario}, timeout=7)
        return run.returncode, json.loads(run.stdout)

    def test_html_and_pdf_candidates(self):
        self.assertEqual(self.run_cli('html','--contains','Unique source')[0], 0)
        code, result = self.run_cli('pdf','--kind','pdf')
        self.assertEqual((code, result['classification']), (0, 'pdf_candidate'))

    def test_refused_and_disguised_challenge(self):
        for scenario, expected in [('forbidden','http_refused'),('challenge','possible_challenge')]:
            code, result = self.run_cli(scenario, '--contains','Unique source')
            self.assertEqual((code,result['classification']), (10,expected))

    def test_wrong_content_and_missing_identity(self):
        for scenario, args, expected in [
            ('false_pdf',['--kind','pdf'],'unexpected_content'),
            ('html',['--contains','Missing record'],'expected_text_not_observed'),
            ('html',[],'html_requires_content_check'),
            ('oversize',['--kind','pdf'],'response_exceeds_limit'),
            ('redirect',[],'redirect_not_followed'),
            ('error',[],'http_error')]:
            code,result=self.run_cli(scenario,*args)
            self.assertEqual((code,result['classification']), (11,expected))

    def test_wall_clock_deadline(self):
        started = time.monotonic()
        code, result = self.run_cli('hang','--timeout','1')
        self.assertEqual((code,result['classification']), (11,'timeout'))
        self.assertLess(time.monotonic()-started, 5)
        self.assertEqual(result['response_file_bytes'], len(b'%PDF-partial'))
        self.assertEqual(result['bytes_read'], 0)
        response_path = Path(self.path_log.read_text())
        self.assertFalse(response_path.exists())
        self.assertFalse(response_path.parent.exists())

    def test_exit_zero_oversized_pdf_is_rejected_before_reading(self):
        code, result = self.run_cli('oversize_exit_zero', '--kind','pdf','--max-bytes','1024')
        self.assertEqual((code,result['classification']), (11,'response_exceeds_limit'))
        self.assertEqual(result['curl_exit_code'], 0)
        self.assertEqual(result['response_file_bytes'], 4101)
        self.assertEqual(result['bytes_read'], 0)
        self.assertFalse(Path(self.path_log.read_text()).parent.exists())

    def test_curl_timeout_partial_body_is_not_read(self):
        code, result = self.run_cli('curl_timeout', '--kind','pdf')
        self.assertEqual((code,result['classification']), (11,'timeout'))
        self.assertEqual(result['response_file_bytes'], len(b'%PDF-partial'))
        self.assertEqual(result['bytes_read'], 0)
        self.assertFalse(Path(self.path_log.read_text()).parent.exists())

    def test_disallowed_urls_before_transport(self):
        for url in ['https://example.org/','http://aaa.org.hk/','https://name:secret@aaa.org.hk/',
                    'https://aaa.org.hk/?token=secret','https://aaa.org.hk:8443/']:
            run = subprocess.run([sys.executable,str(SCRIPT),url], capture_output=True, env=self.env)
            self.assertEqual(run.returncode,2)

    def test_missing_curl_is_explicit(self):
        with patch.object(probe.shutil,'which',return_value=None):
            self.assertEqual(probe.probe('https://aaa.org.hk/','html')['classification'],'curl_unavailable')

if __name__ == '__main__':
    unittest.main(verbosity=2)
