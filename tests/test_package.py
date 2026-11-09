from pathlib import Path
import importlib.util, shutil, tempfile, unittest
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('checker',ROOT/'scripts/check_release.py')
checker=importlib.util.module_from_spec(spec);spec.loader.exec_module(checker)

class PackageTests(unittest.TestCase):
    def test_each_skill_is_standalone(self):
        for skill in (ROOT/'skills').iterdir():
            with self.subTest(skill=skill.name),tempfile.TemporaryDirectory() as tmp:
                isolated=Path(tmp)/skill.name;shutil.copytree(skill,isolated)
                self.assertEqual(checker.check_skill(isolated),[])
    def test_collection_has_no_broken_links_or_shared_drift(self):
        self.assertEqual(checker.check(),[])
    def test_standalone_checker_rejects_sibling_dependency(self):
        with tempfile.TemporaryDirectory() as tmp:
            s=Path(tmp)/'demo';s.mkdir();(s/'SKILL.md').write_text('---\nname: demo\ndescription: Example\n---\n[bad](../sibling/rules.md)')
            self.assertTrue(checker.check_skill(s))

if __name__=='__main__':unittest.main()
