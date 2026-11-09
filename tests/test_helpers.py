from pathlib import Path
from datetime import datetime, timedelta, timezone
import copy, json, runpy, subprocess, sys, tempfile, unittest
ROOT=Path(__file__).resolve().parents[1]
S=ROOT/'skills'
G=runpy.run_path(str(S/'upwork-bid-screen/scripts/screen_guard.py'))
N=runpy.run_path(str(S/'upwork-needs-analysis/scripts/summarize_needs.py'))
NOW=datetime(2026,11,9,tzinfo=timezone.utc)

def snapshot(age=0,kind='approved_api'):
    t=(NOW-timedelta(seconds=age)).isoformat()
    return {'check_id':'synthetic','account_id':'test-account','source_kind':kind,'attempted_at':t,
      'fields':{k:{'status':'ok','value':'test-account' if k=='identity' else 25 if k=='connects' else [],'observed_at':t,'source':'synthetic:'+k} for k in G['CORE']}}
def request():
    return {'expected_account':'test-account','now':NOW.isoformat(),'live':{'check_id':'attempt','attempted_at':NOW.isoformat(),'failure_reason':'no approved capability'},'snapshots':[]}
def record(i,buyer=None,budget=None,duplicate=None):
    r=json.loads((S/'upwork-needs-analysis/assets/need.json').read_text())
    r.update(job_id=i,canonical_url=None,source_locator='input:synthetic/'+i,source_kind='user_provided_text',buyer_id=buyer,duplicate_group=duplicate,version=1,source_entry='research',observed_at=NOW.isoformat(),first_observed_at=NOW.isoformat())
    if budget:r['fields']['budget']={'status':'explicit','value':budget,'evidence':'synthetic quote','reason':None}
    return r

class AccountTests(unittest.TestCase):
    def test_live(self):
        q=request();q['live']=snapshot();r=G['account'](q);self.assertEqual(r['status'],'live');self.assertFalse(r['spending_authorized'])
    def test_72_hour_inclusive(self):
        q=request();q['snapshots']=[snapshot(259200)];self.assertEqual(G['account'](q)['status'],'cached')
    def test_over_72_hours(self):
        q=request();q['snapshots']=[snapshot(259201)];self.assertEqual(G['account'](q)['status'],'blocked')
    def test_configured_age(self):
        q=request();q.update(max_age_hours=1,snapshots=[snapshot(3600)]);self.assertEqual(G['account'](q)['status'],'cached');q['snapshots']=[snapshot(3601)];self.assertEqual(G['account'](q)['status'],'blocked')
    def test_zero_disables_cache(self):
        q=request();q.update(max_age_hours=0,snapshots=[snapshot()]);self.assertEqual(G['account'](q)['status'],'blocked')
    def test_invalid_age(self):
        for age in [-1,True,'72',float('inf')]:
            q=request();q['max_age_hours']=age
            with self.subTest(age=age),self.assertRaises(ValueError):G['account'](q)
    def test_account_mismatch_overrides_cache(self):
        q=request();q['live']=snapshot();q['live']['account_id']='other';q['snapshots']=[snapshot()];self.assertEqual(G['account'](q)['reason'],'observed_account_mismatch')
    def test_export_never_live(self):
        q=request();q['live']=snapshot(kind='user_provided_export');r=G['account'](q);self.assertEqual(r['status'],'cached');self.assertEqual(r['source_kind'],'user_provided_export')
    def test_legacy_never_live(self):
        q=request();q['live']=snapshot();del q['live']['source_kind'];self.assertEqual(G['account'](q)['status'],'cached')
    def test_invalid_future_snapshot(self):
        q=request();q['snapshots']=[snapshot(-1)];self.assertEqual(G['account'](q)['status'],'blocked')
    def test_incomplete_snapshot(self):
        q=request();s=snapshot();s['fields']['offers']['status']='unknown';q['snapshots']=[s];self.assertEqual(G['account'](q)['status'],'blocked')
    def test_newer_partial_balance_and_applications(self):
        q=request();q['snapshots']=[snapshot(1000)];live=snapshot();live['fields']['contracts']['status']='unknown';live['fields']['connects']['value']=4;live['fields']['applications']['value']=[{'job_id':'sent','status':'submitted'},{'job_id':'draft','status':'draft'}];q['live']=live
        r=G['account'](q);self.assertEqual(r['status'],'cached');self.assertEqual(r['balance'],25);self.assertEqual(r['conservative_balance_before_unreconciled_spending'],4);self.assertEqual(r['excluded_job_ids'],['sent'])
    def test_local_submission_and_withdrawal_excluded(self):
        q=request();q['live']=snapshot();q['local_submissions']=[{'account_id':'test-account','job_id':'local','status':'withdrawn','submitted_at':NOW.isoformat(),'source':'synthetic'}];self.assertEqual(G['account'](q)['excluded_job_ids'],['local'])
    def test_local_different_account_rejected(self):
        q=request();q['live']=snapshot();q['local_submissions']=[{'account_id':'other','job_id':'x','submitted_at':NOW.isoformat(),'source':'synthetic'}]
        with self.assertRaises(ValueError):G['account'](q)
    def test_zero_balance_valid(self):
        q=request();q['live']=snapshot();q['live']['fields']['connects']['value']=0;self.assertEqual(G['account'](q)['status'],'live')
    def test_bool_balance_invalid(self):
        q=request();q['live']=snapshot();q['live']['fields']['connects']['value']=False;self.assertEqual(G['account'](q)['status'],'blocked')

class ConfigTests(unittest.TestCase):
    def setUp(self):self.template=G['load_preferences'](S/'upwork-bid-screen/assets/preferences.md')
    def test_blank_valid(self):G['validate'](self.template,self.template)
    def test_legacy_defaults_do_not_mutate_saved_file(self):
        t=copy.deepcopy(self.template);del t['platform_filters'];G['validate'](t,self.template);self.assertNotIn('platform_filters',t)
    def test_arbitrary_nonempty_source_feed(self):
        t=copy.deepcopy(self.template);t['platform_filters']['feed']['value']='approved-source-custom';G['validate'](t,self.template)
    def test_inverted_hard_bounds(self):
        t=copy.deepcopy(self.template);t['contract']['budget_min']={'value':200,'mode':'hard'};t['contract']['budget_max']={'value':100,'mode':'hard'}
        with self.assertRaises(ValueError):G['validate'](t,self.template)
    def test_override_is_run_only(self):
        path=S/'upwork-bid-screen/assets/preferences.md';before=path.read_bytes();r=G['config']({'path':str(path),'overrides':{'capacity':{'hours_per_week':{'value':4,'mode':'hard'}}}});self.assertEqual(r['effective']['capacity']['hours_per_week']['value'],4);self.assertEqual(path.read_bytes(),before)
    def test_duplicate_yaml_key(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/'prefs.md';p.write_text('---\nversion: 1\nversion: 2\n---\n')
            with self.assertRaises(ValueError):G['load_preferences'](p)
    def test_unknown_override(self):
        with self.assertRaises(ValueError):G['config']({'path':str(S/'upwork-bid-screen/assets/preferences.md'),'overrides':{'invalid':{}}})

class NeedsTests(unittest.TestCase):
    def test_dedup_unknown_buyers_and_budget_denominators(self):
        a=record('A','buyer',{'type':'fixed','currency':'EUR','amount':100},'same');b=record('B','buyer',{'type':'fixed','currency':'EUR','amount':100},'same');a2=copy.deepcopy(a);a2['version']=2;a2['observed_at']=(NOW+timedelta(seconds=1)).isoformat();c=record('C',budget={'type':'hourly','currency':'USD','min':30,'max':40});d=record('D')
        r=N['summarize']([a,b,a2,c,d]);self.assertEqual((r['input_versions'],r['unique_jobs'],r['need_groups']),(5,4,3));self.assertEqual(r['known_distinct_buyers'],1);self.assertEqual(r['unknown_buyer_jobs'],2);self.assertEqual(r['budget_missing_ratio'],1/3);self.assertEqual(set(r['posted_budgets']),{'fixed/EUR','hourly/USD'})
    def test_equal_time_conflict(self):
        a=record('A');b=copy.deepcopy(a);b['version']=2
        with self.assertRaises(ValueError):N['summarize']([a,b])
    def test_inference_not_counted_as_posted_budget(self):
        a=record('A');a['fields']['budget']={'status':'inferred','value':200,'reason':'synthetic estimate','evidence':None};r=N['summarize']([a]);self.assertEqual(r['posted_budgets'],{});self.assertEqual(r['budget_missing_by_status'],{'inferred':1})
    def test_empty_is_not_market_absence(self):self.assertEqual(N['summarize']([])['unique_jobs'],0)
    def test_old_url_records_work(self):
        a=record('A');del a['source_locator'];a['canonical_url']='https://example.invalid/jobs/A';self.assertEqual(N['summarize']([a])['unique_jobs'],1)
    def test_unknown_buyer_duplicates_not_collapsed(self):
        self.assertEqual(N['summarize']([record('A',duplicate='same'),record('B',duplicate='same')])['need_groups'],2)
    def test_explicit_fact_needs_evidence(self):
        a=record('A');a['fields']['pain']={'status':'explicit','value':'slow','evidence':None,'reason':None}
        with self.assertRaises(ValueError):N['summarize']([a])

class MilestoneTests(unittest.TestCase):
    def run_helper(self,*args):return subprocess.run([sys.executable,str(S/'upwork-proposal/scripts/validate_milestones.py'),*args],capture_output=True,text=True)
    def test_no_default_limit(self):
        r=self.run_helper('x'*500);self.assertEqual(r.returncode,0);self.assertIn('NOT_ENFORCED',r.stdout)
    def test_inclusive_limit(self):
        self.assertEqual(self.run_helper('--max-chars','200','x'*200).returncode,0);self.assertEqual(self.run_helper('--max-chars','200','x'*201).returncode,1)
    def test_legacy_limit(self):self.assertEqual(self.run_helper('--max-chars','199','x'*200).returncode,1)
    def test_unicode_codepoints(self):
        r=self.run_helper('--max-chars','4','中文á😀');self.assertEqual(r.returncode,0);self.assertIn('4 code points',r.stdout)
    def test_empty_invalid(self):self.assertEqual(self.run_helper('').returncode,1)
    def test_invalid_limit(self):self.assertEqual(self.run_helper('--max-chars','0','a').returncode,2)

if __name__=='__main__':unittest.main()
