import json, pytest
from harness import load, UserError

@pytest.fixture
def env(): return load('civic_signal.py','CivicSignal')

def test_open_verify_close(env):
    _, c, _, q, w, _ = env
    c.open_incident('INC-1','Payments API','Payments are intermittently failing for some users.','https://status.example/inc','https://postmortem.example/inc','https://advisory.example/inc')
    bodies=['status says impact is resolved and the service is operating normally','postmortem says the incident is closed after mitigation and follow-up','advisory confirms recovery and gives the next monitoring step']
    w.extend(bodies + bodies)
    q.extend(['{"status":"RESOLVED","summary":"The incident is closed.","next_step":"Monitor the next release."}'] * 2)
    c.verify_incident('inc-1')
    c.close_incident('INC-1')
    r=json.loads(c.get_incident('0xowner','INC-1'))
    assert r['state']=='CLOSED' and r['signal']=='RESOLVED' and len(r['digests'])==3

def test_distinct_hosts_and_close_guard(env):
    _, c, _, _, _, _ = env
    with pytest.raises(UserError): c.open_incident('INC-1','API','This incident summary is long enough for validation.','https://same.example/a','https://same.example/b','https://same.example/c')
    c.open_incident('INC-2','API','This incident summary is long enough for validation.','https://status.example/a','https://postmortem.example/b','https://advisory.example/c')
    with pytest.raises(UserError): c.close_incident('INC-2')

def test_bad_consensus_fails(env):
    _, c, _, q, w, _ = env
    c.open_incident('INC-3','API','This incident summary is long enough for validation.','https://status.example/a','https://postmortem.example/b','https://advisory.example/c')
    w.extend(['status body is sufficiently long for testing','postmortem body is sufficiently long for testing','advisory body is sufficiently long for testing'])
    q.append('{}')
    with pytest.raises((ValueError,UserError)): c.verify_incident('INC-3')

def test_recheck_accepts_equivalent_status_with_different_wording(env):
 _,c,gl,q,w,p=env
 c.open_incident('INC-4','API','This incident summary is long enough for validation.','https://status.example/a','https://postmortem.example/b','https://advisory.example/c')
 bodies=['x'*50,'y'*50,'z'*50]; w.extend(bodies*4)
 q.extend(['{"status":"ACTIVE","summary":"First wording is different.","next_step":"Keep watching the service."}','{"status":"ACTIVE","summary":"Validator used another wording.","next_step":"Continue monitoring."}'])
 c.verify_incident('INC-4')
 q.extend(['{"status":"RESOLVED","summary":"Resolved after follow-up.","next_step":"Archive the incident."}','{"status":"RESOLVED","summary":"Different prose, same decision.","next_step":"Keep the record."}'])
 c.verify_incident('INC-4'); c.close_incident('INC-4')
 r=json.loads(c.get_incident('0xowner','INC-4')); assert r['state']=='CLOSED' and r['verification_count']==2 and len(r['history'])==2

def test_harmless_transport_difference_is_tolerated(env):
 _,c,gl,q,w,p=env
 c.open_incident('INC-5','API','This incident summary is long enough for validation.','https://status.example/a','https://postmortem.example/b','https://advisory.example/c')
 leader=['status says resolved and service is operating normally.\n\n','postmortem says resolved after mitigation and follow-up.\n','advisory says resolved and monitoring continues.\n']
 validator=['  status   says resolved and service is operating normally.  \n','postmortem says resolved after mitigation and follow-up.\n\n','advisory says resolved and monitoring continues.  ']
 w.extend(leader+validator); q.extend(['{"status":"RESOLVED","summary":"The incident is resolved.","next_step":"Monitor recovery."}']*2)
 c.verify_incident('INC-5'); r=json.loads(c.get_incident('0xowner','INC-5'))
 assert r['signal']=='RESOLVED' and r['digests']==[__import__('hashlib').sha256(x.strip().encode()).hexdigest() for x in leader]
 assert len(r['raw_digests'])==3

def test_material_difference_still_fails(env):
 _,c,gl,q,w,p=env
 c.open_incident('INC-6','API','This incident summary is long enough for validation.','https://status.example/a','https://postmortem.example/b','https://advisory.example/c')
 w.extend(['status says resolved and service is operating normally.','postmortem says resolved after mitigation and follow-up.','advisory says resolved and monitoring continues.','status says ongoing impact affects users right now.','postmortem says ongoing impact remains unresolved.','advisory says ongoing impact is still being investigated.'])
 q.extend(['{"status":"RESOLVED","summary":"The incident is resolved.","next_step":"Monitor recovery."}','{"status":"ACTIVE","summary":"The incident is still active.","next_step":"Continue monitoring."}'])
 with pytest.raises(UserError): c.verify_incident('INC-6')
 assert json.loads(c.get_incident('0xowner','INC-6'))['state']=='OPEN'

def test_harmless_html_and_metadata_churn_is_tolerated(env):
 _,c,gl,q,w,p=env
 c.open_incident('INC-7','API','This incident summary is long enough for validation.','https://status.example/a','https://postmortem.example/b','https://advisory.example/c')
 leader=['<main><p>Service recovered and monitoring continues. The incident remains under observation for follow-up work.</p></main>','<article>Incident closed after mitigation. The postmortem records the recovery and follow-up actions.</article>','<div>Recovery confirmed. Independent advisory confirms normal service and continued monitoring.</div>']
 validator=['<main data-rendered="2026-10-07T10:00:00Z"><p>Service recovered and monitoring continues. The incident remains under observation for follow-up work.</p><script>window.now=1</script></main>','<!-- generated --><article class="fresh">Incident closed after mitigation. The postmortem records the recovery and follow-up actions.</article>','<div data-cache="b7">Recovery confirmed. Independent advisory confirms normal service and continued monitoring.</div>']
 w.extend(leader+validator)
 q.extend(['{"status":"RESOLVED","summary":"The incident is resolved.","next_step":"Monitor recovery."}']*2)
 c.verify_incident('INC-7')
 r=json.loads(c.get_incident('0xowner','INC-7'))
 assert r['state']=='VERIFIED' and r['signal']=='RESOLVED'
